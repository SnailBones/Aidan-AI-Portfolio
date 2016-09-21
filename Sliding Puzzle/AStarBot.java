import java.util.Random;
import java.util.ArrayList;
import java.util.HashSet;
import java.lang.Math;
import java.util.PriorityQueue;

// SlidingBoard has a public field called size
// A size of 3 means a 3x3 board

// SlidingBoard has a method to getLegalMoves
//   ArrayList<SlidingMove> legalMoves = board.getLegalMoves();

// You can create possible moves using SlidingMove:
// This moves the piece at (row, col) into the empty slot
//   SlidingMove move = new SlidingMove(row, col);

// SlidingBoard can check a single SlidingMove for legality:
//   boolean legal = board.isLegalMove(move);

// SlidingBoard can check if a position is a winning one:
//   boolean hasWon = board.isSolved();

// SlidingBoard can perform a SlidingMove:
//   board.doMove(move);

// You can undo a move by saying the direction of the previous move
// For example, to undo the last move that moved a piece down into
// the empty space from above use:
//   board.undoMove(m, 0);

// You can dump the board to view with toString:
//   System.out.println(board);
class SlideNode implements Comparable {
  SlidingBoard board;
  ArrayList <SlidingMove> moves;
  public double cost;
  public SlideNode(SlidingBoard b, ArrayList <SlidingMove> m, SlidingBoard end)
  {
    board = b;
    moves = m;
    double endDist = GuessDistance(b,end);
    cost = endDist + m.size();

  }
  public int compareTo(Object otherNode) {
    SlideNode other = (SlideNode) otherNode;
    return new Double(cost).compareTo(new Double(other.cost));
  }
  public ArrayList <SlidingMove> getNewMoves()
  {
    return board.getLegalMoves();
  }
  public int Manhattan (int x1, int y1, int x2, int y2)
  {
    return Math.abs(x1-x2) + Math.abs(y1-y2);
  }
  //returns distance from number at x,y on b1 to same number on b2
  public int FindDist (int x1, int y1, int[][] b1, int[][] b2)
  {
    int myNum = b1[x1][y1];
    for (int r = 0; r<b2.length; r++)
    {
      for (int c = 0; c<b2.length; c++)
      {
        if (b2[r][c] == myNum)
          return Manhattan(x1,y1,r,c);
      }
    }
    return -1;
  }
  public int GuessDistance(SlidingBoard b1, SlidingBoard b2)
  {
    int total = 0;
    for (int r = 0; r<b1.size; r++)
    {
      for (int c = 0; c<b1.size; c++)
      {
        if (b1.board[r][c] != b2.board[r][c])
        {
          int dist = FindDist (r, c, b1.board, b2.board);
          total += dist;
        }
      }
    }
    return total;
  }
}

class AStarBot extends SlidingPlayer {
    public static ArrayList <SlidingMove> solution;
    HashSet<String> seen = new HashSet<String>();
    // The constructor gets the initial board
    public AStarBot(SlidingBoard _sb) {
        super(_sb);
        solution = makeNodes(_sb);
    }
    public ArrayList <SlidingMove> makeNodes(SlidingBoard _sb){
      SlidingBoard end = new SlidingBoard(_sb.size); //moved here for efficiency
      end.initBoard();
      PriorityQueue<SlideNode> nodePile = new PriorityQueue<SlideNode>();
      SlideNode firstNode =  new SlideNode(_sb, new ArrayList<SlidingMove>(),end); //create the mother node
      nodePile.add(firstNode);
      seen.add(firstNode.toString());

      //ArrayList <SlidingMove> movesSoFar = myNode.moves;
      //SlidingBoard myboard;
      while (nodePile.size()>0)  //until solved
      {
        SlideNode myNode = nodePile.poll();
        //System.out.println("node pile: " + nodePile);
        //System.out.println(myNode.board.toString());
        if (myNode.board.isSolved())
        {
          System.out.println("solved!");
          return myNode.moves;
        }
        if (myNode.moves.size() < 50)
        {
          for (SlidingMove move: myNode.board.getLegalMoves()) //for every possible move
          {
            //System.out.println("building node pile. size = " + myNode.moves.size());
            SlidingBoard newBoard = new SlidingBoard(myNode.board.size);
            newBoard.setBoard(myNode.board);
            newBoard.doMove(move);
            if (!seen.contains(newBoard.toString())) {
              seen.add(newBoard.toString());
              ArrayList<SlidingMove> childMoves = (ArrayList<SlidingMove>)myNode.moves.clone(); //add all moves to queue
              childMoves.add(move);
              SlideNode newNode = new SlideNode(newBoard,childMoves,end); //add new Node
              nodePile.add(newNode);
              //set myNode to new node
            }
          }
        }
      }
      System.out.println("failed to find a solution :(!");
      return null;
    }
    //Perform a move
    public SlidingMove makeMove(SlidingBoard board) {
      return solution.remove(0);
    }
}
