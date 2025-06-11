import java.awt.*;
import java.util.ArrayList;

public class Enemy
{
    //Enemy Aggro Level
    private int aggrevationLevel;
    
    //Enemy Location
    private Point enemyLoc;
    
    //Enemy path variables
    private ArrayList<Point> waypoints;
    private int direction;
    private int completion;
    
    //Enemy hitboxes
    private Rectangle enemySightHitBox;
    private Rectangle enemyHitBox;
    
    //universal size
    private final int SIZE;
    
    public Enemy(Point enemyLoc, ArrayList<Point> waypoints)
    {
        aggrevationLevel = 0;
        this.enemyLoc = enemyLoc;
        this.waypoints = waypoints;
        completion = 0;
        direction = 0;
        SIZE = 40;
        enemySightHitBox = new Rectangle((int) enemyLoc.getX() + 100, (int) enemyLoc.getY() - 80, 70, 80);
        enemyHitBox = new Rectangle((int) enemyLoc.getX(), (int) enemyLoc.getY(), SIZE, SIZE);
    }
    
    //Changes enemy movement to continue in a direction until it reaches a waypoint where it continuously moves in the new direction of a waypoint, then goes back to its original point somehow and repeats
    public void updateEnemyMovement()
    {
        switch (direction)
        {
            //Start direction or waypoint completed direction
            case 0:
                if(getEnemyLoc().getY() < waypoints.get(completion).getY())
                    direction = 1;
                else if(getEnemyLoc().getX() > waypoints.get(completion).getX())
                    direction = 2;
                else if(getEnemyLoc().getY() > waypoints.get(completion).getY())
                    direction = 3;
                else if(getEnemyLoc().getX() < waypoints.get(completion).getX())
                    direction = 4;
                break;
            //Down
            case 1:
                enemyLoc.translate(0, 1);
                if(getEnemyLoc().getY() == waypoints.get(completion).getY())
                {
                    completion = (completion + 1) % waypoints.size();
                    direction = 0;
                }
                break;
            //Left
            case 2:
                enemyLoc.translate(-1, 0);
                if(getEnemyLoc().getX() == waypoints.get(completion).getX())
                {
                    completion = (completion + 1) % waypoints.size();
                    direction = 0;
                }
                break;
            //Up
            case 3:
                enemyLoc.translate(0, -1);
                if(getEnemyLoc().getY() == waypoints.get(completion).getY())
                {
                    completion = (completion + 1) % waypoints.size();
                    direction = 0;
                }
                break;
            //Right
            case 4:
                enemyLoc.translate(1, 0);
                if(getEnemyLoc().getX() == waypoints.get(completion).getX())
                {
                    completion = (completion + 1) % waypoints.size();
                    direction = 0;
                }
                break;
        }
        //Updates vision hit box to avoid canvas clutter
        updateSightHitBox();
    }
    
    //Changes aggro level of enemy
    public void setAggro(int num)
    {
        aggrevationLevel = num;
    }
    
    //Returns aggro level of enemy
    public int getAggro()
    {
        return aggrevationLevel;
    }
    
    //Returns location of crate
    public Point getEnemyLoc()
    {
        return enemyLoc;
    }
    
    //Returns hit box of enemy
    public Rectangle getEnemyHitBox()
    {
        enemyHitBox.setLocation((int) enemyLoc.getX(), (int) enemyLoc.getY());
        return enemyHitBox;
    }
    
    //Keeps the vision of enemies in from of them in somewhat reasonable manner
    public void updateSightHitBox()
    {
        switch (direction)
        {
            case 0:
                break;
            case 1:
                enemySightHitBox.setLocation((int) enemyLoc.getX() - 20, (int) enemyLoc.getY() + SIZE);
                break;
            case 2:
                enemySightHitBox.setLocation((int) enemyLoc.getX() - 70, (int) enemyLoc.getY() - 20);
                break;
            case 3:
                enemySightHitBox.setLocation((int) enemyLoc.getX() - 15, (int) enemyLoc.getY() - 60);
                break;
            case 4:
               enemySightHitBox.setLocation((int) enemyLoc.getX() + SIZE, (int) enemyLoc.getY() - 20);
                break;
        }
    }
    
    //Returns the sight hit box
    public Rectangle getSightHitBox()
    {
        return enemySightHitBox;
    }
}