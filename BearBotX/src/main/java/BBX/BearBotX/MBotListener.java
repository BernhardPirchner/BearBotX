package BBX.BearBotX;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class MBotListener implements Runnable {
    private ServerSocket server=null;
    private ArrayList<String> list=new ArrayList<>();

    public MBotListener(){
        try {
            server = new ServerSocket(6970);
            run();
        }catch(Exception ex){
            System.out.println(ex.getMessage());
        }
    }

    public ArrayList<String> getDevices(){
        return list;
    }

    @Override
    public void run() {
        while(true){
            Socket client=null;
            list.add("Ich bin der BearBot!, 10.10.2.120");

            try{
                client=server.accept();
                Scanner in =new Scanner(client.getInputStream());
                String s=in.nextLine();
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
            }catch(Exception ex){
                System.out.println();
            }
        }
    }

    public ArrayList<String> getList(){
        return list;
    }
}