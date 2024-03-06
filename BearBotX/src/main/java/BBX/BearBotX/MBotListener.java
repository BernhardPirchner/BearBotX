package BBX.BearBotX;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class MBotListener {
    //Auf Server umstellen
    ServerSocket server=null;
    ArrayList<String> list=new ArrayList<>();

    public MBotListener(){
        try {
            server = new ServerSocket(6970);
            Scanner in = new Scanner(server.getInputStream());
            Thread thread = new Thread() {
                public void run() {
                    String s = "";
                    while (true) {
                        s = in.nextLine();
                        if (!list.contains(s)) {
                            list.add(s);
                        }
                    }
                }
            };
            thread.run();
        }catch(Exception ex){
            System.out.println(ex.getMessage());
        }
    }

    public ArrayList<String> getDevices(){
        return list;
    }
}