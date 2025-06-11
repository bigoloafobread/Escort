import java.awt.*;

public class Crate
{
    //Crate location/hitbox
    private Point crateLoc;
    private Rectangle crateHitBox;
    
    //Universal size
    private final int SIZE;
    
    public Crate(Point crateLoc)
    {
        SIZE = 40;
        this.crateLoc = crateLoc;
        crateHitBox = new Rectangle((int) crateLoc.getX(), (int) crateLoc.getY(), SIZE - 10, SIZE - 10);
    }
    
    //Returns location of crate
    public Point getCrateLoc()
    {
        return crateLoc;
    }
    
    //Returns crate hitbox
    public Rectangle getCrateHitBox()
    {
        crateHitBox.setLocation((int) crateLoc.getX(), (int) crateLoc.getY());
        return crateHitBox;
    }
    
    //Sets crate location
    public void setCrateLoc(Point loc)
    {
        crateLoc = loc;
    }
}