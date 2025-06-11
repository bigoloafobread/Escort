import java.awt.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import javax.swing.*;

public class Door
{
    //Door hitbox/location
    private Rectangle doorHitBox;
    private boolean horizontal;
    
    //Door Image
    private Image doorIm;
    
    //Door Identificaiton
    private int doorID;
    private int doorType;
    
    
    public Door(Rectangle doorHitBox, boolean horizontal, int doorID, int doorType)
    {
        this.doorHitBox = doorHitBox;
        this.horizontal = horizontal;
        this.doorID = doorID;
        this.doorType = doorType;
        //Horizontal
        if (horizontal)
        {
            doorIm = new ImageIcon("Door_Asset.png").getImage().getScaledInstance(80, 10, Image.SCALE_SMOOTH);
        }
        //Locked Door
        else if (doorType == 1)
        {
             doorIm = new ImageIcon("Locked_Door_Asset.png").getImage().getScaledInstance(10,80, Image.SCALE_SMOOTH);
        }
        //Vertical
        else
        {
            doorIm = new ImageIcon("Door_Asset.png").getImage().getScaledInstance(10, 80, Image.SCALE_SMOOTH);
        }
        
    }
    
    //Returns door hitbox
    public Rectangle getDoorHitBox()
    {
        return doorHitBox;
    }
    
    //Sets locked/unlocked door status
    public void setDoorType(int num)
    {
        doorType = num;
    }
    
    //Helps render the door to the hitbox
    public boolean isHorizontal()
    {
        return horizontal;
    }
    
    //Returns door image
    public Image getDoorIm()
    {
        return doorIm;
    }
    
    //Returns unique door ID to be linked
    public int getDoorID()
    {
        return doorID;
    }
    
    
}