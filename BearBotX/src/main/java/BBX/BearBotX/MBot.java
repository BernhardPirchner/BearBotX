package BBX.BearBotX;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.*;
import java.util.Scanner;

public class MBot {
    Socket server=null;
    Scanner in=null;
    PrintWriter out=null;

    public MBot(){

    }

    public String listen() throws IOException {
        server  =new Socket("10.10.3.255", 6969);
        in=new Scanner(server.getInputStream());
        return in.nextLine();
    }

    public String connect(String ip) {
        try{
            server=new Socket(ip, 6969);
            in=new Scanner(server.getInputStream());
            out=new PrintWriter(server.getOutputStream());
            return "Connection successful";
        }catch(Exception ex){
            System.out.println("Exception:\n"+ ex.getMessage());
            return "Connection unsuccessful";
        }
    }

    public void send(String s){
        if(server != null) {
            try {
                out.println(s);
            } catch (Exception ex) {
                System.out.println(ex.getMessage());
            }
        }
    }

    public String getData(){
        out.println("hole Daten");
        return in.nextLine();
    }

    public String closeConnection(){
        String answer="Disconnection was unsuccessful";
        if(server!=null){
            try{
                server.close();
                answer="Disconnection was successful";
            }catch(Exception ex){
                answer= "Disconnection was unsuccessful\nException: "+ex.getMessage();
            }
        }
        return answer;
    }
}
