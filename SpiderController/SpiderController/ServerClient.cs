using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace SpiderController
{
    class ServerClient
    {
        StreamWriter bufferedStream;
        StreamReader reader;
        TcpClient tcpClient;
        public ServerClient()
        {
            tcpClient = new TcpClient();
            
            tcpClient.Connect("192.168.10.1", 15);
            //tcpClient.Connect("192.168.10.1", 15);*/
            var networkStream = tcpClient.GetStream();
            bufferedStream = new StreamWriter(networkStream);
            reader = new StreamReader(networkStream);
            List<string> paramList = new List<string>();
            paramList.Clear();
            paramList.Add("gamepad");
            sendMessage(Command.IDENTYFY, paramList);
            sendMessage(Command.TO_MANUAL, null);
            Thread t = new Thread(run);
            t.Start();

        }

        public void run()
        {
            try
            {
                while (true)
                {
                    string text = reader.ReadLine();
                    //Console.WriteLine(text);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("Connection Lost!!!");
            }

        }

        public void sendMessage(int Command, List<string> parameters)
        {
            String line = "";
            if (parameters != null && parameters.Count > 0)
            {
                line = Command.ToString() + "<;>";
                foreach (string obj in parameters)
                {
                    line += obj + "<;>";
                }
            }
            else
            {
                line = Command.ToString() + "<;>";
            }
            Console.WriteLine(line);
           // byte[] byteArray =Encoding.ASCII.GetBytes(line);
            bufferedStream.WriteLine(line);
            bufferedStream.Flush();
        }
    }
}