using Renci.SshNet;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
namespace SpiderDashboard
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        ServerClient client;
        public MainWindow()
        {
            InitializeComponent();
            client = null;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            client = new ServerClient(this);
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            if (client != null)
            {
                client.sendMessage(Command.KILL, null);
         
            }
        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            log_textBox.Text = "";
        }
        SshClient ssh;
        private void Button_Click_3(object sender, RoutedEventArgs e)
        {
            Instellingen inst = new Instellingen();
            ConnectionInfo connectionInfo = new PasswordConnectionInfo(inst.ip, "pi", "idpgroep5");
             ssh = new SshClient(connectionInfo);
            
                ssh.Connect();
                var cmd = ssh.CreateCommand("./startSpinOS.sh");   //  very long list
                var asynch = cmd.BeginExecute();
                System.Threading.Thread.Sleep(20000);
                ssh.Disconnect();

            
            /*SshStream ssh = new SshStream("192.168.10.1", "pi", "idpgroep5");
            //Set the end of response matcher character
            ssh.Prompt = "#";
            //Remove terminal emulation characters
            ssh.RemoveTerminalEmulationCharacters = true;
            //Writing to the SSH channel
            ssh.Write("./startSpinOS.sh");*/
        }

        private void Button_Click_4(object sender, RoutedEventArgs e)
        {
            Instellingen inst = new Instellingen();
            string input = Microsoft.VisualBasic.Interaction.InputBox("Geeft ip", "Change ip", inst.ip, -1, -1);
            inst.ip = input;
            inst.Save();
        }
    }
}
