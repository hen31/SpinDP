using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;

namespace SpiderDashboard
{
    class ServerClient
    {
        StreamWriter bufferedStream;
        StreamReader reader;
        TcpClient tcpClient;
        private MainWindow mainWindow;
        public ServerClient(MainWindow mainWindow)
        {
            tcpClient = new TcpClient();
            Instellingen inst = new Instellingen();
            tcpClient.Connect(inst.ip, 15);
            //tcpClient.Connect("192.168.10.1", 15);*/
            var networkStream = tcpClient.GetStream();
            bufferedStream = new StreamWriter(networkStream);
            reader = new StreamReader(networkStream);
            List<string> paramList = new List<string>();
            paramList.Clear();
            paramList.Add("dashboard");
            sendMessage(Command.IDENTYFY, paramList);
            sendMessage(Command.TO_MANUAL, null);
            this.mainWindow = mainWindow;
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
                    string[] parts = text.Split(new string[] { "<;>" }, StringSplitOptions.RemoveEmptyEntries);
                    if (parts[0] == "10")
                    {
                        mainWindow.Dispatcher.Invoke(new Action(delegate
                        {
                            mainWindow.log_textBox.Text += parts[1] + Environment.NewLine;
                            mainWindow.log_textBox.ScrollToEnd();
                        }));

                    }

                    //Console.WriteLine(text);
                }
            }
            catch (Exception e)
            {
                MessageBox.Show("Connectie verloren");
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