import javax.swing.*; // No Partner
import java.awt.*;
import java.awt.event.*;
import java.awt.Color;

public class MyProgram {
    
    //Screen Size
    public static final int WIDTH = 600; 
    public static final int HEIGHT = 600;

    //Mainly untouched rendering bits
    public static void main(String[] args) {
        JFrame f= new JFrame();

        Canvas canvas = new Canvas(WIDTH, HEIGHT); 
        canvas.setPreferredSize(new Dimension(WIDTH,HEIGHT)); 
        f.getContentPane().setBackground(Color.BLACK);
        
        f.add(canvas); 
        f.pack(); 
        f.setVisible(true);
    }
}