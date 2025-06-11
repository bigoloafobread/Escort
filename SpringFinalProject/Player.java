import java.awt.*;

public class Player
{
    //Player enviormental statuses
    private boolean isHidden;
    private boolean caught;
    
    //Player location/hitboxes
    private Point playerLoc;
    private Rectangle playerWallColHitBox;
    private Rectangle playerHitBox;
    
    //Player facing direction
    private int wallVal;
    
    //Universal size
    private final int SIZE;
    
    //Movement speed
    private int moveRatio;
    
    //Movement conditions
    private boolean moveUp;
    private boolean moveDown;
    private boolean moveLeft;
    private boolean moveRight;
    
    //Key possession status
    private boolean hasKey1;
    
    
    public Player()
    {
        moveRatio = 2;
        isHidden = false;
        SIZE = 40;
        
        wallVal = 1;
        
        moveUp = false;
        moveDown = false;
        moveLeft = false;
        moveRight = false;
        
        caught = false;
        
        hasKey1 = false;
        
        playerLoc = new Point(150, 150);
        playerHitBox = new Rectangle((int) playerLoc.getX(), (int) playerLoc.getY(), SIZE, SIZE);
        playerWallColHitBox = new Rectangle((int) playerLoc.getX() + SIZE, (int) playerLoc.getY(), 10, SIZE);
    }
    
    //Returns player location
    public Point getLoc()
    {
        return playerLoc;
    }
    
    //Sets player location
    public void setLoc(Point loc)
    {
        playerLoc = loc;
    }
    
    //Returns player facing direction
    public int getWallVal()
    {
        return wallVal;
    }
    
    //Sets player facing direction
    public void setWallVal(int num)
    {
        wallVal = num;
    }
    
    //Returns player key status
    public boolean getKey1()
    {
        return hasKey1;
    }
    
    //Sets player key status
    public void setKey1(boolean thing)
    {
        hasKey1 = thing;
    }
    
    //Returns player hitbox
    public Rectangle getPlayerHitBox()
    {
        playerHitBox.setLocation((int) playerLoc.getX(), (int) playerLoc.getY());
        return playerHitBox;
    }
    
    //Returns player wall collision hitbox
    public Rectangle getPlayerWallColHitBox()
    {
        return playerWallColHitBox;
    }
    
    //Sets player wall collision hitbox
    public void setPlayerWallColHitBox()
    {
        if (moveRight) 
        {
            playerWallColHitBox = new Rectangle((int) playerLoc.getX() + SIZE - 10, (int) playerLoc.getY() + 5, 10, SIZE - 10);
        }
        else if (moveLeft) 
        {
            playerWallColHitBox = new Rectangle((int) playerLoc.getX(), (int) playerLoc.getY() + 5, 10, SIZE - 10);
        }
        else if (moveUp) 
        {
            playerWallColHitBox = new Rectangle((int) playerLoc.getX() + 5, (int) playerLoc.getY(), SIZE - 10, 10);
        }
        else if (moveDown) 
        {
            playerWallColHitBox = new Rectangle((int) playerLoc.getX() + 5, (int) playerLoc.getY() + SIZE - 10, SIZE - 10, 10);
        }
    }
    
    //Moves player what direction it needs
    public void updatePlayerMovement() 
    {
        if (moveRight) 
        {
            playerLoc.translate(moveRatio, 0);
        }
        if (moveLeft) 
        {
            playerLoc.translate(-moveRatio, 0);
        }
        if (moveUp) 
        {
            playerLoc.translate(0, -moveRatio);
        }
        if (moveDown) 
        {
            playerLoc.translate(0, moveRatio);
        }
        
    }
    
    //triggers player movement
    public void setMoveRight(boolean value) 
    { 
        moveRight = value; 
    }
    public void setMoveLeft(boolean value) 
    { 
        moveLeft = value;
    }
    public void setMoveUp(boolean value) 
    { 
        moveUp = value; 
    }
    public void setMoveDown(boolean value) 
    {
        moveDown = value;
    }
    
    //Hides the player
    public void hidePlayer()
    {
        isHidden = true;
    }
    
    //Reveals the player
    public void revealPlayer()
    {
        isHidden = false;
    }
    
    //Sets caught status of player
    public void setCaught(boolean val)
    {
        caught = val;
    }
    
    //Returns caught status of player
    public boolean getCaught()
    {
        return caught;
    }
    
    //Returns player hidden status
    public boolean getPlayerHiddenCondition()
    {
        return isHidden;
    }
}