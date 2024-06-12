package BBX.BearBotX;

import java.io.IOException;
import java.net.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class MBotListener implements Runnable {
    DatagramSocket socket=null;
    private static ArrayList<String> list=new ArrayList<>();

    public MBotListener() {
        try {
            socket=new DatagramSocket(6970);
            socket.setBroadcast(true);
            list.add("10.10.1.1");
            list.add("10.10.255.255");
            run();
        }catch(Exception ex){
            System.out.println(ex.getMessage());
        }
    }

    @Override
    public void run() {
        byte[] buffer=new byte[1024];
        DatagramPacket packet=new DatagramPacket(buffer, buffer.length);
        while(true){
            try{
                socket.receive(packet);
                String s=new String(packet.getData(), 0, packet.getLength());
                System.out.println(s);

                boolean x=true;
                for (String bot:
                        list) {
                    if(bot.equals(s)) {
                        x = false;
                    }
                }
                if(x){
                    list.add(s);
                }

                packet.setLength(buffer.length);
            }catch(Exception ex){
                System.out.println(ex.getMessage());
            }
        }
    }

    public ArrayList<String> getList(){
        return list;
    }

    public static ArrayList<String> getDevices(){
        return list;
    }
}