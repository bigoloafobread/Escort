import java.awt.*;

public class Key
{
    //Key location
    private Point keyLoc;
    
    //Key hitbox
    private Rectangle keyHitBox;
    
    //Universal size
    private final int SIZE;
    
    public Key(Point keyLoc)
    {
        SIZE = 40;
        this.keyLoc = keyLoc;
        keyHitBox = new Rectangle((int) keyLoc.getX(), (int) keyLoc.getY(), SIZE - 10, SIZE - 10);
    }
    
    //Returns key location
    public Point getKeyLoc()
    {
        return keyLoc;
    }
    
    //Returns key hitbox
    public Rectangle getKeyHitBox()
    {
        keyHitBox.setLocation((int) keyLoc.getX(), (int) keyLoc.getY());
        return keyHitBox;
    }
    
    //Sets key location
    public void setkeyLoc(Point loc)
    {
        keyLoc = loc;
    }
}