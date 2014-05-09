using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Input;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SpiderController
{
    class Program
    {
        static void Main(string[] args)
        {
            GamePadState gamePadState = GamePad.GetState(PlayerIndex.One);
            GamePadState previousPadState = GamePad.GetState(PlayerIndex.One);
            ServerClient client = new ServerClient();

            bool internalMode = false;
            int previousHeight = -109203;
            while (gamePadState.IsConnected)
            {
                gamePadState = GamePad.GetState(PlayerIndex.One);
                Vector2 rightStickDirection = gamePadState.ThumbSticks.Right;
                int strengthRight = (int)(rightStickDirection.Length() * 100);
                int angleRight = 0;
                float thumbX = rightStickDirection.X;
                float thumbY = -rightStickDirection.Y;
                angleRight = (int)((float)Math.Atan2(thumbY, thumbX) * (180 / Math.PI));
                angleRight += 90;
                if (angleRight < 0)
                {
                    angleRight += 360;
                }
                Vector2 leftStickDirection = gamePadState.ThumbSticks.Left;

                int strengthLeft = (int)(leftStickDirection.Length() * 100);
                int angleLeft = 0;
                thumbX = leftStickDirection.X;
                thumbY = -leftStickDirection.Y;
                angleLeft = (int)((float)Math.Atan2(thumbY, thumbX) * (180 / Math.PI));
                angleLeft += 90;
                if (angleLeft < 0)
                {
                    angleLeft += 360;
                }

                if (leftStickDirection.X == 0 && leftStickDirection.Y == 0)
                {
                    strengthLeft = 0;
                    angleLeft = 0;
                }
                if (rightStickDirection.X == 0 && rightStickDirection.Y == 0)
                {
                    strengthRight = 0;
                    angleRight = 0;
                }
                if (internalMode)
                {
                    List<string> _temp = new List<string>();
                    if (previousPadState.ThumbSticks.Left.X != leftStickDirection.X || previousPadState.ThumbSticks.Left.Y != leftStickDirection.Y)
                    {

                        _temp.Add(angleLeft.ToString());
                        _temp.Add(strengthLeft.ToString());
                        _temp.Add("0");
                        _temp.Add("0");
                        client.sendMessage(Command.MOVE, _temp);
                    }
                    if (previousPadState.ThumbSticks.Right.X != rightStickDirection.X || previousPadState.ThumbSticks.Right.Y != rightStickDirection.Y)
                    {
                        _temp.Clear();
                        _temp.Add(angleRight.ToString());
                        _temp.Add(strengthRight.ToString());
                        client.sendMessage(Command.MOVE_INTERNAL, _temp);
                    }
                }
                else
                {
                    if (previousPadState.ThumbSticks.Left.X != leftStickDirection.X || previousPadState.ThumbSticks.Left.Y != leftStickDirection.Y
                        || previousPadState.ThumbSticks.Right.X != rightStickDirection.X || previousPadState.ThumbSticks.Right.Y != rightStickDirection.Y)
                    {
                        List<string> _temp = new List<string>();
                        _temp.Add(angleLeft.ToString());
                        _temp.Add(strengthLeft.ToString());
                        _temp.Add(angleRight.ToString());
                        _temp.Add(strengthRight.ToString());
                        client.sendMessage(Command.MOVE, _temp);
                    }
                }
                if (gamePadState.IsButtonDown(Buttons.A) && previousPadState.IsButtonUp(Buttons.A))
                {
                    client.sendMessage(Command.TO_MANUAL, null);
                }
                if (gamePadState.IsButtonDown(Buttons.B) && previousPadState.IsButtonUp(Buttons.B))
                {
                    client.sendMessage(Command.TO_BALLOON_MODE, null);
                }
                if (gamePadState.IsButtonDown(Buttons.X) && previousPadState.IsButtonUp(Buttons.X))
                {
                    internalMode = !internalMode;
                }
                if (gamePadState.IsButtonDown(Buttons.Y) && previousPadState.IsButtonUp(Buttons.Y))
                {
                    client.sendMessage(Command.TO_TEERBAL_MODE, null);
                }
                if (gamePadState.IsButtonDown(Buttons.LeftShoulder) && previousPadState.IsButtonUp(Buttons.LeftShoulder))
                {
                    client.sendMessage(Command.KILL, null);
                }
                int leftValue = (int)(gamePadState.Triggers.Left * 100);
                int rightValue = (int)(gamePadState.Triggers.Right * 100);
                int currentHeight = 50  + rightValue/2 - leftValue/2;
                if (currentHeight < 0)
                {
                    currentHeight += 100;
                }
                if (currentHeight != previousHeight)
                {
                    previousHeight = currentHeight;
                    client.sendMessage(Command.MOVE_HEIGHT, new List<string>() { currentHeight.ToString() });
                }
                previousPadState = gamePadState;
            }


        }
    }
}