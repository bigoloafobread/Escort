import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.net.URL;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.util.ArrayList;

public class Canvas extends JComponent{ 
    //Images
    private Image playerIm; 
    private Image playerImHidden;
    private Image crateIm;
    private Image enemyIm;
    private Image testIm;
    private Image gameScreen;
    private Image keyIm;
    private Image gameOverScreen;
    private Image victoryScreen;
    private Image instructions;
    
    //Universal size
    private static final int SIZE = 40;
    
    //Screen Size
    private final int HEIGHT;
    private final int WIDTH;
    
    //Time Variables
    private static final int ONE_SECOND = 1000;
    private static final int GAME_LENGTH = 3;
    private int time;
    
    //Win/Lose Conditions
    private boolean gameOver;
    private boolean escorted;
    
    //Custom Objects
    private Player player;
    private Room room;
    
    
    //Dev Stuff
    private boolean devMode;
    
    public Canvas(int width, int height) {
        Toolkit tk = Toolkit.getDefaultToolkit();
        
        //Image Initilizations
        playerIm = new ImageIcon("Player_Asset.png").getImage().getScaledInstance(SIZE, SIZE, Image.SCALE_SMOOTH);
        playerImHidden = new ImageIcon("Hidden_Asset.png").getImage().getScaledInstance(SIZE, SIZE, Image.SCALE_SMOOTH);
        crateIm = new ImageIcon("Crate_Asset.png").getImage().getScaledInstance(SIZE, SIZE, Image.SCALE_SMOOTH);
        enemyIm = new ImageIcon("Enemy_Asset.png").getImage().getScaledInstance(SIZE, SIZE, Image.SCALE_SMOOTH);
        testIm = new ImageIcon("Crate_Asset.png").getImage().getScaledInstance(SIZE, SIZE, Image.SCALE_SMOOTH);
        gameScreen = new ImageIcon("Screen_Border_Asset.png").getImage().getScaledInstance(400, 400, Image.SCALE_SMOOTH);
        keyIm = new ImageIcon("Key_Asset.png").getImage().getScaledInstance(SIZE, SIZE, Image.SCALE_SMOOTH);
        gameOverScreen = new ImageIcon("Game_Over_Asset.png").getImage().getScaledInstance(600, 600, Image.SCALE_SMOOTH);
        victoryScreen = new ImageIcon("Victory_Asset.png").getImage().getScaledInstance(600, 600, Image.SCALE_SMOOTH);
        instructions = new ImageIcon("Instructions_Asset.png").getImage().getScaledInstance(600, 600, Image.SCALE_SMOOTH);
        
    
        //Screen Size
        WIDTH = width; 
        HEIGHT = height; 
        
        //Detection Time
        time = GAME_LENGTH; 
        
        //End Game Status
        gameOver = false;
        escorted = false;
        
        //Player/Room Initializations
        player = new Player();
        room = new Room();
        room.room1();
        
        //Set this to true to see some cool hitboxes
        devMode = false;
            
        
        //Mouse stuff (Unused)
        class Mickey implements MouseListener
        {
            public void mouseClicked(MouseEvent e){}
            public void mouseEntered(MouseEvent e){}
            public void mouseExited(MouseEvent e){}
            public void mousePressed(MouseEvent e){}
            public void mouseReleased(MouseEvent e){}
        }
        
        class KBListener implements KeyListener
        {
            //Game Reset Key
            public void keyTyped(KeyEvent e)
            {
                if (e.getKeyChar() == 'r')
                {
                    player.setLoc(new Point(150, 150));
                    player.setKey1(false);
                    room.room1();
                    room.lock();
                    gameOver = false;
                    escorted = false;
                    player.setCaught(false);
                    time = GAME_LENGTH;
                    
                    for (int i = 0; i < room.getEnemies().size(); i++)
                    {
                        room.getEnemies().get(i).setAggro(0);
                    }
                }
                repaint();
                
            }
            //WASD Movement trigger and wall check activations
            public void keyPressed(KeyEvent e){
                for (int i = 0; i < room.getWalls().size(); i++)
                {
                    if (e.getKeyChar() == 'd' && ((checkWallCollision(player, room.getWalls().get(i)) && player.getWallVal() != 3) || !checkWallCollision(player, room.getWalls().get(i))))
                    {
                        player.setWallVal(3);
                        player.setMoveRight(true);
                    }
                    else if (e.getKeyChar() == 'a' && ((checkWallCollision(player, room.getWalls().get(i)) && player.getWallVal() != 2) || !checkWallCollision(player, room.getWalls().get(i))))
                    {
                        player.setWallVal(2);
                        player.setMoveLeft(true);
                    }
                    else if (e.getKeyChar() == 'w' && ((checkWallCollision(player, room.getWalls().get(i)) && player.getWallVal() != 1) || !checkWallCollision(player, room.getWalls().get(i))))
                    {
                        player.setWallVal(1);
                        player.setMoveUp(true);
                    }
                    else if (e.getKeyChar() == 's' && ((checkWallCollision(player, room.getWalls().get(i)) && player.getWallVal() != 4) || !checkWallCollision(player, room.getWalls().get(i))))
                    {
                        player.setWallVal(4);
                        player.setMoveDown(true);
                    }
                }
                repaint();
            }
            
            //Release Key Inaction
            public void keyReleased(KeyEvent e)
            {
                if (e.getKeyChar() == 'd')
                {
                    player.setMoveRight(false);
                }
                else if (e.getKeyChar() == 'a')
                {
                    player.setMoveLeft(false);
                }
                else if (e.getKeyChar() == 'w')
                {
                    player.setMoveUp(false);
                }
                else if (e.getKeyChar() == 's')
                {
                    player.setMoveDown(false);
                }
                repaint();
            }
        }
        addKeyListener(new KBListener());
        setFocusable(true);
        this.requestFocus();
        
        //Enemy and Player Movement Timer
        Timer gameTimer = new Timer(16, e -> 
        {
            if (!checkPlayerWallCollision(player)) 
            {
                player.updatePlayerMovement();
            }
            else 
            {
                resolvePlayerWallCollision(player);
            }
            
            for (int i = 0; i < room.getEnemies().size(); i++)
            {
                room.getEnemies().get(i).updateEnemyMovement();
            }
            repaint();
        });
        gameTimer.start();
        
        //Aggro Level 1 to 2 Timer
        Timer detectTimer;
        class detectListener implements ActionListener
        {
            public void actionPerformed(ActionEvent e)
            {
                for (int i = 0; i < room.getEnemies().size(); i++)
                {
                    if (room.getEnemies().get(i).getAggro() == 1)
                    {
                        time--;
                    }
                    if (time == 0)
                    {
                        room.getEnemies().get(i).setAggro(2);
                    }
                }
            }
        }
        detectTimer = new Timer(ONE_SECOND, new detectListener());
        detectTimer.start();
    } 
    
    //COLLISION METHODS **************************************************
    
    //Determines Directional availbility of player movement when colliding a wall
    public void resolvePlayerWallCollision(Player player) 
    {
        for (Wall wall:room.getWalls()) 
        {
            Rectangle wallBox = wall.getWallHitBox();
            if (player.getPlayerWallColHitBox().intersects(wallBox)) 
            {
                switch (player.getWallVal()) 
                {
                    case 1:
                        player.setMoveUp(false);
                        break;
                    case 2:
                        player.setMoveLeft(false);
                        break;
                    case 3:
                        player.setMoveRight(false);
                        break;
                    case 4:
                        player.setMoveDown(false);
                        break;
                }
            }
        }
    }

    //Checks Wall Collisions with Player
    public boolean checkPlayerWallCollision(Player player) 
    {
        for (Wall wall:room.getWalls()) 
        {
            if (player.getPlayerWallColHitBox().intersects(wall.getWallHitBox())) 
                return true;
        }
        return false;
    }
    
    //Checks Enemy Collisions with Player
    public boolean checkEnemyCollision(Player player, Enemy enemy)
    {
        //Collision Check
        if (player.getPlayerHitBox().intersects(enemy.getEnemyHitBox()))
            return true;
        else
            return false;
    }
    
    //Checks Enemy Vision Collisions with Player
    public boolean checkEnemySightCollision(Player player, Enemy enemy)
    {
        //Collision Check
        if (player.getPlayerHitBox().intersects(enemy.getSightHitBox()))
            return true;
        else
            return false;
    }
    
    //Checks Wall Collisions with Player
    public boolean checkWallCollision(Player player, Wall wall)
    {
        if (player.getPlayerWallColHitBox().intersects(wall.getWallHitBox()))
            return true;
        else
            return false;
    }
        
    //Checks Crate Collisions with Player
    public void checkCrateCollision(Player player, Crate crate)
    {
        if (player.getPlayerHitBox().intersects(crate.getCrateHitBox()) == true)
            player.hidePlayer();
        else
            player.revealPlayer();
    }
    
    //Checks Key Collisions with Player
    public boolean checkKeyCollision(Player player, Key key)
    {
        if (player.getPlayerHitBox().intersects(key.getKeyHitBox()))
        {
            room.unlock();
            player.setKey1(true);
            return true;
        }
        else
            return false;
    }
    
    public void checkDoorCollision(Player player, Door door)
    {
        if (player.getPlayerHitBox().intersects(door.getDoorHitBox()))
        {
            switch (door.getDoorID()) 
            {
                case 1: //To 4, (2, 2) - (1, 2), Linked
                    room.room2();
                    player.setLoc(new Point(445, 380));
                    break;
                case 2: //To 15, (2, 2) - (3, 2), Linked
                    room.room7();
                    player.setLoc(new Point(125, 385));
                    break;
                case 3: //To 6, (1, 2) - (1, 1), Linked
                    room.room3();
                    player.setLoc(new Point(420, 450));
                    break;
                case 4: //To 1, (1, 2) - (2, 2), Linked
                    room.room1();
                    player.setLoc(new Point(125, 380));
                    break;
                case 5: //To 7 (1, 2) - (1, 3), Linked
                    room.room4();
                    player.setLoc(new Point(135, 115));
                    break;
                case 6: //To 3, (1, 1) - (1, 2), Linked
                    room.room2();
                    player.setLoc(new Point(420, 115));
                    break;
                case 7: //To 5, (1, 3) - (1, 2), Linked
                    room.room2();
                    player.setLoc(new Point(135, 445));
                    break;
                case 8: //To 10, (1, 3) - (2, 3), Linked
                    room.room5();
                    player.setLoc(new Point(125, 335));
                    break;
                case 9: //To 22, (1, 3) - (1, 4), Linked
                    room.room10();
                    player.setLoc(new Point(420, 115));
                    break;
                case 10: //To 8, (2, 3) - (1, 3), Linked
                    room.room4();
                    player.setLoc(new Point(445, 335));
                    break;
                case 11: //To 12, (2, 3) - (3, 3), Linked
                    room.room6();
                    player.setLoc(new Point(125, 335));
                    break;
                case 12: //To 11, (3, 3) - (2, 3), Linked
                    room.room5();
                    player.setLoc(new Point(445, 335));
                    break;
                case 13: //To 18, (3, 3) - (3, 4), Linked
                    room.room8();
                    player.setLoc(new Point(425, 115));
                    break;
                case 14: //To 16, (3, 3) - (3, 2), Linked
                    room.room7();
                    player.setLoc(new Point(425, 450));
                    break;
                case 15: //To 2, (3, 2) - (2, 2), Linked
                    room.room1();
                    player.setLoc(new Point(435, 385));
                    break;
                case 16: //To 14, (3, 2) - (3, 3), Linked
                    room.room6();
                    player.setLoc(new Point(425, 125));
                    break;
                case 17: //To 19, (3, 4) - (2, 4), Linked
                    room.room9();
                    player.setLoc(new Point(435, 125));
                    break;
                case 18: //To 13, (3, 4) - (3, 3), Linked
                    room.room6();
                    player.setLoc(new Point(425, 435));
                    break;
                case 19: //To 17, (2, 4) - (3, 4), Linked
                    room.room8();
                    player.setLoc(new Point(125, 125));
                    break;
                case 20: //To 23, (2, 4) - (1, 4), Linked
                    room.room10();
                    player.setLoc(new Point(435, 315));
                    break;
                case 21: //To 24, (2, 4) - (1, 4), Linked
                    room.room10();
                    player.setLoc(new Point(445, 425));
                    break;
                case 22: //To 9, (1, 4) - (1, 3), Linked
                    room.room4();
                    player.setLoc(new Point(420, 445));
                    break;
                case 23: //To 20, (1, 4) - (2, 4), Linked
                    room.room9();
                    player.setLoc(new Point(125, 315));
                    break;
                case 24: //To 21, (1, 4) - (2, 4), Linked
                    room.room9();
                    player.setLoc(new Point(125, 425));
                    break;
                case 100: //To 101, (3, 3) - Ending, 
                    if (player.getKey1())
                    {
                        room.room11();
                        player.setLoc(new Point(125, 280));
                        escorted = true;
                        break;
                    }
                    else
                        break;
                case 101: //To 100, Ending - (3, 3)
                    room.room6();
                    player.setLoc(new Point(435, 280));
                    break;
                    
            }
        }
    }
    
    
    //Render Section *****************************************************
    public void paintComponent(Graphics grr)
    {
        Graphics2D g = (Graphics2D) grr;
        
        //Checks for player hitting a wall
        player.setPlayerWallColHitBox();
        
        //Player Hidden Display
        if (player.getPlayerHiddenCondition() == false)
        {
            g.drawImage(playerIm, (int) player.getLoc().getX(), (int) player.getLoc().getY() ,this);
        }
        else if (player.getPlayerHiddenCondition() == true)
        {
            g.drawImage(playerImHidden, (int) player.getLoc().getX(), (int) player.getLoc().getY() ,this);
        }
        
        
        //Enemy Display and Mechanics Per Room
        for (int i = 0; i < room.getEnemies().size(); i++)
        {
            g.drawImage(enemyIm, (int) room.getEnemies().get(i).getEnemyLoc().getX(), (int) room.getEnemies().get(i).getEnemyLoc().getY(), this);
            if (!player.getPlayerHiddenCondition())
            {
                //Aggro Level 2
                if (checkEnemyCollision(player, room.getEnemies().get(i)) || room.getEnemies().get(i).getAggro() == 2)
                {
                    g.setFont(new java.awt.Font("Arial", java.awt.Font.BOLD, 45));
                    g.setColor(java.awt.Color.RED);
                    g.drawString("!", (int) room.getEnemies().get(i).getEnemyLoc().getX() + 12, (int) room.getEnemies().get(i).getEnemyLoc().getY());
                    player.setCaught(true);
                }
                //Aggro Level 1
                else if (checkEnemySightCollision(player, room.getEnemies().get(i)))
                {
                    g.setFont(new java.awt.Font("Arial", java.awt.Font.BOLD, 45));
                    g.setColor(java.awt.Color.YELLOW);
                    g.drawString("?", (int) room.getEnemies().get(i).getEnemyLoc().getX() + 10, (int) room.getEnemies().get(i).getEnemyLoc().getY());
                    room.getEnemies().get(i).setAggro(1);
                }
            }
            //Enemy Sight Hitboxes
            if (devMode)
            {
                g.setColor(Color.MAGENTA); // Enemy
                Rectangle sightBox = room.getEnemies().get(i).getSightHitBox();
                g.drawRect(sightBox.x, sightBox.y, sightBox.width, sightBox.height);
            }
            
        }
        
        //Crate Display/Mechanics Per Room
        boolean hidden = false;
        for (int i = 0; i < room.getCrates().size(); i++)
        {
            if (player.getPlayerHitBox().intersects(room.getCrates().get(i).getCrateHitBox())) 
            {
                hidden = true;
            }
            g.drawImage(crateIm, (int) room.getCrates().get(i).getCrateLoc().getX(), (int) room.getCrates().get(i).getCrateLoc().getY(), this);
        }
        if (hidden) 
            player.hidePlayer();
        else 
            player.revealPlayer();
        
        //Wall Display and Mechanics Per Room
        for (int i = 4; i < room.getWalls().size(); i++)
        {
            g.drawImage(room.getWalls().get(i).getWallIm(), (int) room.getWalls().get(i).getWallHitBox().x, (int) room.getWalls().get(i).getWallHitBox().y, this);
        }
        
        //Key Rendering
        for (int i = 0; i < room.getKeys().size(); i++)
        {
            if (!checkKeyCollision(player, room.getKeys().get(i)) && !player.getKey1())
                g.drawImage(keyIm, (int) room.getKeys().get(i).getKeyHitBox().x, (int) room.getKeys().get(i).getKeyHitBox().y, this);
        }
        
        //Dev Visual Testing ***************************
        if (devMode)
        {
            g.setColor(Color.BLUE); //Player Direction/Wall
            Rectangle wallBox = player.getPlayerWallColHitBox();
            g.drawRect(wallBox.x, wallBox.y, wallBox.width, wallBox.height);
        }
        
        //Screen Border Render
        g.drawImage(gameScreen, 100, 100, this); 
        
        //Door Display and Collision Detection
        for (int i = 0; i < room.getDoors().size(); i++)
        {
             g.drawImage(room.getDoors().get(i).getDoorIm(), (int) room.getDoors().get(i).getDoorHitBox().x, (int) room.getDoors().get(i).getDoorHitBox().y, this);
             checkDoorCollision(player, room.getDoors().get(i));
        }
        
        
        //Instructions
        g.drawImage(instructions, 0, 0, this);
        
        //End Game Screens
        if (player.getCaught())
        {
            gameOver = true;
            g.drawImage(gameOverScreen, 0, 0, this);
        }
        if (escorted)
        {
            g.drawImage(victoryScreen, 0, 0, this);
        }
    }
    
 
}