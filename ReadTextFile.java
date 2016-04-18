import java.io.*;
import java.util.*;

public class ReadTextFile{
  public static void main(String[] args) {
    String pwd = getCurrentDirectory();
    String filePath = pwd + "/Songs/love_train.txt";
    ArrayList allSongs = new ArrayList();
    allSongs.add(getSongWordList(filePath));
    System.out.println(allSongs.get(0));
  }

  public static String getCurrentDirectory(){
    String dir = System.getProperty("user.dir");
    return dir;
  }

  public static ArrayList<String> getSongWordList(String filePath){
    ArrayList<String> retVal = new ArrayList<>();
    try{
      FileReader inputFile = new FileReader(filePath);
      BufferedReader bufferReader = new BufferedReader(inputFile);
      String line;
      String song="";
      while((line = bufferReader.readLine())!=null){
        line = line.trim();
        if(line.length() != 0){
          song = song + " " + line;
        }
      }
      String[] songText = song.replaceAll("[^a-zA-Z ]", "").toLowerCase().split("\\s+");
      retVal = new ArrayList(Arrays.asList(songText));
      bufferReader.close();
    }
    catch(Exception e){
      System.out.println("Error while reading file line by line:" + e.getMessage());
    }

    return retVal;
  }
}
