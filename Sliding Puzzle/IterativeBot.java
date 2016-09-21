import java.util.Random;
import java.util.ArrayList;
import java.util.HashSet;

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
class SlideNode {
  SlidingBoard board;
  ArrayList <SlidingMove> moves;
  public SlideNode(SlidingBoard b, ArrayList <SlidingMove> m)
  {
    board = b;
    moves = m;
  }
  public ArrayList <SlidingMove> getNewMoves()
  {
    return board.getLegalMoves();
  }
  // public Object clone() throws CloneNotSupportedException {
  //   SlideNode slClone = (SlideNode)super.clone();
  //   return slClone;
  // }
}

class IterativeBot extends SlidingPlayer {
    public static ArrayList <SlidingMove> solution;
    ArrayList<SlideNode> nodePile;
    // The constructor gets the initial board
    public IterativeBot(SlidingBoard _sb) {
        super(_sb);
        solution = makeNodes(_sb);
    }
    public ArrayList <SlidingMove> makeNodes(SlidingBoard _sb){
      int cur_max = 0;
      while (true)
      {
        ArrayList <SlideNode> nodePile = new ArrayList<SlideNode>();
        SlideNode firstNode =  new SlideNode(_sb, new ArrayList<SlidingMove>()); //create the mother node
        HashSet<String> seen = new HashSet<String>();
        nodePile.add(firstNode);
        seen.add(firstNode.toString());

        //ArrayList <SlidingMove> movesSoFar = myNode.moves;
        //SlidingBoard myboard;
        System.out.println("size is "+nodePile.size());
        while (nodePile.size()>0)  //until solved
        {
          SlideNode myNode = nodePile.remove(nodePile.size()-1);
          System.out.println("size is "+nodePile.size());
          System.out.println(myNode.board.toString());
          if (myNode.board.isSolved())
          {
            System.out.println("solved!");
            return myNode.moves;
          }
          if (myNode.moves.size() <= cur_max)
          {
            System.out.println("checking");
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
                SlideNode newNode = new SlideNode(newBoard,childMoves); //add new Node
                nodePile.add(newNode);
                //set myNode to new node
              }
            }
          }
        }
        cur_max++;
        System.out.println("searching again with max: "+cur_max);
      }
    }
    //Perform a move
    public SlidingMove makeMove(SlidingBoard board) {
      return solution.remove(0);
    }
}
