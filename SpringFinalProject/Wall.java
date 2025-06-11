import java.awt.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import javax.swing.*;

public class Wall
{
    private Rectangle wallHitBox;
    private Image wallIm;
    
    //stretches walls to fit hitboxes automatically
    public Wall(Rectangle wallHitBox)
    {
        this.wallHitBox = wallHitBox;
        wallIm = new ImageIcon("Wall_Asset.png").getImage().getScaledInstance(wallHitBox.width, wallHitBox.height, Image.SCALE_SMOOTH);
        
    }
    
    //Returns hit box of wall
    public Rectangle getWallHitBox()
    {
        return wallHitBox;
    }
    
    //Returns image of wall
    public Image getWallIm()
    {
        return wallIm;
    }
    
}