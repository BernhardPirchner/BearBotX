package BBX.BearBotX;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class MBot {
    Socket server=null;
    Scanner in=null;
    PrintWriter out=null;

    public MBot(){

    }

    public String connect(String ip) {
        try{
            server=new Socket(ip, 6969);
            in=new Scanner(server.getInputStream());
            out=new PrintWriter(server.getOutputStream(), true);
            return "Connection successful";
        }catch(Exception ex){
            System.out.println("Exception:\n"+ ex.getMessage());
            return "Connection unsuccessful";
        }
    }

    public void send(String s){
        if(server != null) {
            try {
                //System.out.println("Hallo");
                out.println(s);
            } catch (Exception ex) {
                System.out.println("sendException");
                System.out.println(ex.getMessage());
            }
        }
    }

    public String getData(String s){
        if(server!=null){
            try{
                send(s);
                String answer= in.nextLine();
                System.out.println(answer);
                return answer;
            }catch(Exception ex){
                System.out.println(ex.getMessage());
                return "{\"Error\":\"No_line\",\"Cause\":\""+ex.getMessage().replace(' ', '_')+"\"}";
            }
        }
        //System.out.println("{\"Error\":\"Not_Connected\"}");
        return "{\"Error\":\"Not_Connected\"}";
    }

    public String disconnect(){
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
