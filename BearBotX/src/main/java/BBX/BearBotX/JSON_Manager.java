package BBX.BearBotX;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class JSON_Manager {
    public String[] toStringArray(String json){
        String[] text=json.split("[\"{:}]");
        //System.out.println("1");
        ArrayList<String> temp= new ArrayList<String>();
        for (String s:
             text) {
            temp.add(s);
        }
        //System.out.println("2");
        temp.removeAll(Arrays.asList(" ", "", null));
        //System.out.println("3");
        for (String s:
             text) {
            //System.out.println(s);
        }
        return temp.toArray(new String[0]);
    }
}
