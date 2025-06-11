import java.util.ArrayList;
import java.awt.*;


public class Room
{
    //Arrays for any room objects
    private ArrayList<Enemy> roomEnemies;
    private ArrayList<Crate> roomCrates;
    private ArrayList<Wall> roomWalls;
    private ArrayList<Door> roomDoors;
    private ArrayList<Key> roomKeys;
    
    //Enemy path storage
    private ArrayList<ArrayList<Point>> enemyPaths;
    
    //Locked door status
    private boolean unlocked;
    
    
    public Room()
    {
        this.roomEnemies = new ArrayList<Enemy>();
        this.roomCrates = new ArrayList<Crate>();
        this.roomWalls = new ArrayList<Wall>();
        this.roomDoors = new ArrayList<Door>();
        this.roomKeys = new ArrayList<Key>();
        this.enemyPaths = new ArrayList<ArrayList<Point>>();
        this.unlocked = false;
    }
    
    //Returns list of certain objects in a room
    public ArrayList<Enemy> getEnemies()
    {
        return roomEnemies;
    }
    
    public ArrayList<Crate> getCrates()
    {
        return roomCrates;
    }
    
    public ArrayList<Wall> getWalls()
    {
        return roomWalls;
    }
    
    public ArrayList<Door> getDoors()
    {
        return roomDoors;
    }
    
    public ArrayList<Key> getKeys()
    {
        return roomKeys;
    }
    
    //Returns certain path of a specific enemy
    public ArrayList<Point> getPath(int num)
    {
        return enemyPaths.get(num);
    }
    
    //unlocks the locked door
    public void unlock()
    {
        unlocked = true;
    }
    
    //relocks the locked door
    public void lock()
    {
        unlocked = false;
    }
    
    //Clears room and keeps screen boundaries when transition to new room
    public void clearLists()
    {
        //Clears Room for Next Room
        roomEnemies.clear();
        roomCrates.clear();
        roomWalls.clear();
        roomDoors.clear();
        enemyPaths.clear();
        roomKeys.clear();
        
        //Sets Screen Border Boundaries
        roomWalls.add(new Wall(new Rectangle(105, 85, 400, 20)));
        roomWalls.add(new Wall(new Rectangle(105, 495, 400, 20)));
        roomWalls.add(new Wall(new Rectangle(85, 85, 20, 400)));
        roomWalls.add(new Wall(new Rectangle(495, 85, 20, 400)));
    }
    
    public void room1() //Tile (2, 2)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        
        //Enemy 0 Path
        enemyPaths.get(0).add(new Point(300, 400));
        enemyPaths.get(0).add(new Point(180, 400));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(180, 400), enemyPaths.get(0)));
        
        //Crate
        roomCrates.add(new Crate(new Point(245, 330)));
        
        //Walls
        roomWalls.add(new Wall(new Rectangle(315, 105, 10, 200)));
        roomWalls.add(new Wall(new Rectangle(105, 300, 150, 10)));
        roomWalls.add(new Wall(new Rectangle(410, 185, 10, 230)));
        
        
        //Left Door
        roomDoors.add(new Door(new Rectangle(105, 370, 10, 80), false, 1, 0));
        //Right Door
        roomDoors.add(new Door(new Rectangle(485, 370, 10, 80), false, 2, 0));
    }
    
    public void room2() //Tile (1, 2)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        enemyPaths.add(new ArrayList<>());
        
        //Enemy 0 Path
        enemyPaths.get(0).add(new Point(300, 410));
        enemyPaths.get(0).add(new Point(130, 410));
        
        //Enemy 1 Path
        enemyPaths.get(1).add(new Point(430, 140));
        enemyPaths.get(1).add(new Point(430, 260));
        enemyPaths.get(1).add(new Point(130, 260));
        enemyPaths.get(1).add(new Point(130, 140));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(130, 410), enemyPaths.get(0)));
        
        //Enemy 1
        roomEnemies.add(new Enemy(new Point(130, 140), enemyPaths.get(1)));
        
        //Bottom Section Crates
        roomCrates.add(new Crate(new Point(330, 380)));
        roomCrates.add(new Crate(new Point(200, 380)));
        
        //Top Crate
        roomCrates.add(new Crate(new Point(275, 190)));
        
        //Bottom Section Walls
        roomWalls.add(new Wall(new Rectangle(190, 340, 310, 10)));
        roomWalls.add(new Wall(new Rectangle(415, 340, 10, 100)));
        
        //Top Section Walls
        roomWalls.add(new Wall(new Rectangle(205, 240, 180, 10)));
        roomWalls.add(new Wall(new Rectangle(205, 190, 10, 50)));
        roomWalls.add(new Wall(new Rectangle(375, 190, 10, 50)));
        
        
        //Top Door
        roomDoors.add(new Door(new Rectangle(400, 104, 80, 10), true, 3, 0));
        //Right Door
        roomDoors.add(new Door(new Rectangle(485, 370, 10, 80), false, 4, 0));
        //Bottom Door
         roomDoors.add(new Door(new Rectangle(115, 489, 80, 10), true, 5, 0));
    }
    
    public void room3() //Tile (1,1)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        enemyPaths.add(new ArrayList<>());
        enemyPaths.add(new ArrayList<>());
        enemyPaths.add(new ArrayList<>());
        enemyPaths.add(new ArrayList<>());
        enemyPaths.add(new ArrayList<>());
        enemyPaths.add(new ArrayList<>());
        
        //Enemies Non-Movement
        enemyPaths.get(0).add(new Point(180, 340));
        enemyPaths.get(1).add(new Point(230, 300));
        enemyPaths.get(2).add(new Point(220, 360));
        enemyPaths.get(3).add(new Point(200, 200));
        enemyPaths.get(4).add(new Point(360, 210));
        enemyPaths.get(5).add(new Point(400, 180));
        enemyPaths.get(6).add(new Point(410, 370));
        
        //Small Bit of Enemies (No Movement)
        roomEnemies.add(new Enemy(new Point(180, 340), enemyPaths.get(0)));
        roomEnemies.add(new Enemy(new Point(230, 300), enemyPaths.get(1)));
        roomEnemies.add(new Enemy(new Point(220, 360), enemyPaths.get(2)));
        roomEnemies.add(new Enemy(new Point(200, 200), enemyPaths.get(3)));
        roomEnemies.add(new Enemy(new Point(360, 210), enemyPaths.get(4)));
        roomEnemies.add(new Enemy(new Point(400, 180), enemyPaths.get(5)));
        roomEnemies.add(new Enemy(new Point(410, 370), enemyPaths.get(6)));
        
        
        //Top Section Walls
        roomWalls.add(new Wall(new Rectangle(325, 435, 160, 10)));
        roomWalls.add(new Wall(new Rectangle(325, 435, 10, 60)));
        roomWalls.add(new Wall(new Rectangle(480, 435, 10, 60)));
        
        
        //Top Door
        roomDoors.add(new Door(new Rectangle(400, 489, 80, 10), true, 6, 0));

    }
    
    public void room4() //Tile (1, 3)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        
        //Enemy 0 Path
        enemyPaths.get(0).add(new Point(370, 350));
        enemyPaths.get(0).add(new Point(130, 350));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(130, 350), enemyPaths.get(0)));
        
        //Bottom Section Walls
        roomWalls.add(new Wall(new Rectangle(105, 400, 390, 10)));
        
        //Top Section Walls
        roomWalls.add(new Wall(new Rectangle(195, 190, 10, 150)));
        roomWalls.add(new Wall(new Rectangle(295, 190, 10, 150)));
        roomWalls.add(new Wall(new Rectangle(395, 190, 10, 150)));
        
        //Key
        roomKeys.add(new Key(new Point(145, 425)));
        
        //Top Door
        roomDoors.add(new Door(new Rectangle(120, 104, 80, 10), true, 7, 0));
        //Right Door
        roomDoors.add(new Door(new Rectangle(485, 315, 10, 80), false, 8, 0));
        //Bottom Door
         roomDoors.add(new Door(new Rectangle(400, 489, 80, 10), true, 9, 0));
    }
    
    public void room5() //Tile (2, 3)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        
        //Enemies Non-Movement
        enemyPaths.get(0).add(new Point(400, 200));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(400, 200), enemyPaths.get(0)));
        
        //Walls
        roomWalls.add(new Wall(new Rectangle(105, 395, 390, 10)));
        roomWalls.add(new Wall(new Rectangle(105, 305, 390, 10)));
        
        //Left Door
        roomDoors.add(new Door(new Rectangle(105, 315, 10, 80), false, 10, 0));
        //Right Door
        roomDoors.add(new Door(new Rectangle(485, 315, 10, 80), false, 11, 0));
    }
    
    public void room6() //Tile (3, 3)
    {
        clearLists();
        
        //Walls
        roomWalls.add(new Wall(new Rectangle(105, 395, 290, 10)));
        roomWalls.add(new Wall(new Rectangle(395, 395, 10, 100)));
        
        //Left Door
        roomDoors.add(new Door(new Rectangle(105, 315, 10, 80), false, 12, 0));
        //Bottom Door
        roomDoors.add(new Door(new Rectangle(405, 489, 80, 10), true, 13, 0));
        //Top Door
        roomDoors.add(new Door(new Rectangle(405, 104, 80, 10), true, 14, 0));
        
        //The D-O-R-E
        if (!unlocked)
            roomDoors.add(new Door(new Rectangle(485, 260, 10, 80), false, 100, 1));
        else
            roomDoors.add(new Door(new Rectangle(485, 260, 10, 80), false, 100, 0));
    }
    
    public void room7() //Tile (3, 2)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        
        //Enemies Non-Movement
        enemyPaths.get(0).add(new Point(300, 130));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(300, 130), enemyPaths.get(0)));
        
        //Walls
        roomWalls.add(new Wall(new Rectangle(205, 205, 110, 10)));
        roomWalls.add(new Wall(new Rectangle(385, 205, 10, 295)));
        roomWalls.add(new Wall(new Rectangle(205, 205, 10, 295)));
        
        
        //Left Door
        roomDoors.add(new Door(new Rectangle(105, 370, 10, 80), false, 15, 0));
        //Bottom Door
        roomDoors.add(new Door(new Rectangle(405, 489, 80, 10), true, 16, 0));

    }
    
    public void room8() //Tile (3, 4)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        
        //Enemy 0 Path
        enemyPaths.get(0).add(new Point(420, 370));
        enemyPaths.get(0).add(new Point(140, 370));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(140, 370), enemyPaths.get(0)));
        
        //Bottom Section Crates
        roomCrates.add(new Crate(new Point(130, 445)));
        roomCrates.add(new Crate(new Point(230, 445)));
        roomCrates.add(new Crate(new Point(330, 445)));
        roomCrates.add(new Crate(new Point(430, 445)));
        
        //Main Walls
        roomWalls.add(new Wall(new Rectangle(205, 335, 190, 10)));
        roomWalls.add(new Wall(new Rectangle(385, 105, 10, 230)));
        roomWalls.add(new Wall(new Rectangle(205, 105, 10, 230)));
        
        //Segment Walls
        roomWalls.add(new Wall(new Rectangle(195, 425, 10, 70)));
        roomWalls.add(new Wall(new Rectangle(295, 425, 10, 70)));
        roomWalls.add(new Wall(new Rectangle(395, 425, 10, 70)));
        
        //Left Door
        roomDoors.add(new Door(new Rectangle(105, 105, 10, 80), false, 17, 0));
        //Top Door
        roomDoors.add(new Door(new Rectangle(405, 104, 80, 10), true, 18, 0));

    }
    
    public void room9() //Tile (2, 4)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        
        //Enemy 0 Path
        enemyPaths.get(0).add(new Point(420, 420));
        enemyPaths.get(0).add(new Point(420, 300));
        enemyPaths.get(0).add(new Point(280, 300));
        enemyPaths.get(0).add(new Point(420, 300));
        enemyPaths.get(0).add(new Point(420, 420));
        enemyPaths.get(0).add(new Point(200, 420));
        enemyPaths.get(0).add(new Point(280, 420));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(280, 420), enemyPaths.get(0)));
        
        //Crates
        roomCrates.add(new Crate(new Point(230, 450)));
        roomCrates.add(new Crate(new Point(220, 265)));
        roomCrates.add(new Crate(new Point(450, 380)));
        
        //Walls
        roomWalls.add(new Wall(new Rectangle(105, 385, 260, 10)));
        roomWalls.add(new Wall(new Rectangle(335, 245, 160, 10)));
        roomWalls.add(new Wall(new Rectangle(205, 195, 10, 190)));
        
        
        //Right Door
        roomDoors.add(new Door(new Rectangle(485, 105, 10, 80), false, 19, 0));
        //Bottom Left Door
        roomDoors.add(new Door(new Rectangle(105, 300, 10, 80), false, 20, 0));
        //Top Left Door
        roomDoors.add(new Door(new Rectangle(105, 400, 10, 80), false, 21, 0));

    }
    
    public void room10() //Tile (1, 4)
    {
        clearLists();
        
        enemyPaths.add(new ArrayList<>());
        
        //Enemy 0 Path
        enemyPaths.get(0).add(new Point(135, 430));
        enemyPaths.get(0).add(new Point(350, 430));
        enemyPaths.get(0).add(new Point(135, 430));
        enemyPaths.get(0).add(new Point(135, 190));
        enemyPaths.get(0).add(new Point(400, 190));
        enemyPaths.get(0).add(new Point(135, 190));
        
        //Enemy 0
        roomEnemies.add(new Enemy(new Point(135, 190), enemyPaths.get(0)));
        
        //Crates
        roomCrates.add(new Crate(new Point(260, 350)));
        roomCrates.add(new Crate(new Point(260, 270)));
        
        //Walls
        roomWalls.add(new Wall(new Rectangle(365, 385, 130, 10)));
        roomWalls.add(new Wall(new Rectangle(365, 265, 130, 10)));
        
        roomWalls.add(new Wall(new Rectangle(205, 325, 150, 10)));
        
        roomWalls.add(new Wall(new Rectangle(195, 245, 10, 170)));
        roomWalls.add(new Wall(new Rectangle(355, 265, 10, 130)));
        
        roomWalls.add(new Wall(new Rectangle(195, 165, 200, 10)));
        roomWalls.add(new Wall(new Rectangle(385, 105, 10, 60)));
        
        //Top Door
        roomDoors.add(new Door(new Rectangle(405, 104, 80, 10), true, 22, 0));
        //Bottom Right Door
        roomDoors.add(new Door(new Rectangle(485, 300, 10, 80), false, 23, 0));
        //Top Right Door
        roomDoors.add(new Door(new Rectangle(485, 400, 10, 80), false, 24, 0));

    }
    
    public void room11() //Tile (4, 3)
    {
        clearLists();
        
        //Walls
        roomWalls.add(new Wall(new Rectangle(105, 375, 200, 10)));
        roomWalls.add(new Wall(new Rectangle(105, 195, 200, 10)));
        roomWalls.add(new Wall(new Rectangle(305, 195, 10, 190)));

        //Top Right Door
        roomDoors.add(new Door(new Rectangle(105, 260, 10, 80), false, 101, 0));

    }
    
}