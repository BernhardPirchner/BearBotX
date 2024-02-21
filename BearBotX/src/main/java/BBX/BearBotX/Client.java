package BBX.BearBotX;

import java.io.PrintWriter;
import java.net.*;
import java.util.Scanner;

public class Client {
    Socket server=null;
    Scanner in=null;
    PrintWriter out=null;

    public Client(){

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

    /*
    public void Listen(){
        System.out.println(in.nextLine());
    }
    */

    public String send(String s){
        String answer="No Answer";
        if(server != null){
            try{
                out.println(s);
                answer= in.nextLine();
                server.close();
            }catch(Exception ex){
                System.out.println(ex.getMessage());
            }
        }
        return answer;
    }

    public String getData(){
        out.println("hole Daten");
        return in.nextLine();
    }

    public void setSpeed(int velocity){
        out.println("ändere Geschwindigkeit zu: "+velocity);
    }

    private void closeConnection(){
        if(server!=null){
            try{
                server.close();
            }catch(Exception ex){
                System.out.println(ex.getMessage());
            }
        }
    }

}
