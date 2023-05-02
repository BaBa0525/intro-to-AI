from pacman import GameState
from util import PriorityQueue, manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        '''
        In maxlevel, we try to select the max value from the next level(minlevel).
        We first find all the possible actions we can do at this state.
        If we arrive the depth we hope or get win or lose situation, we evaluate its value
        by evalation function.
        Otherwise, we go into the next levels and finally select the max one.
        In minlevel, we do the same thing as maxlevel, but this time we choose the min one.

        To get the best action, we don't do the first maxlevel with function to get all the
        min values generated by the minlevel. Then, we choose all the values that equal the
        maxvalue, and choose one from them randomly.
        '''

        try:
            def maxlevel(gameState, depth):
                cur_depth = depth + 1
                if gameState.isWin() or gameState.isLose() or cur_depth == self.depth:
                    return self.evaluationFunction(gameState)
                maxvalue = -float('inf')
                actions = gameState.getLegalActions(0)
                for action in actions:
                    nextState = gameState.getNextState(0, action)
                    maxvalue = max(maxvalue, minlevel(nextState, cur_depth, 1))
                return maxvalue

            def minlevel(gameState, depth, agentIndex):
                if gameState.isWin() or gameState.isLose():
                    return self.evaluationFunction(gameState)
                minvalue = float('inf')
                actions = gameState.getLegalActions(agentIndex)
                for action in actions:
                    nextState = gameState.getNextState(agentIndex, action)
                    if agentIndex == gameState.getNumAgents()-1:
                        minvalue = min(minvalue, maxlevel(nextState, depth))
                    else:
                        minvalue = min(minvalue, minlevel(nextState, depth, agentIndex+1))
                return minvalue

            actions = gameState.getLegalActions(0)
            scores = []
            for action in actions:
                NextState = gameState.getNextState(0, action)
                score = minlevel(NextState, 0, 1)
                scores.append(score)

            highscore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == highscore]
            chosenIndex = random.choice(bestIndices)

            return actions[chosenIndex]
        except:        
            raise NotImplementedError("To be implemented")
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        '''
        This part does almost the same thing as part1.
        However, we use alpha and beta the record the maxvalue and minvalue that 
        has gotten from other branches on the above level.
        Therefore, we take alpha as an example, if we find a value less than alpha
        in minlevel, than we can't select it because we have a better choice alpha.
        In the situation, we can prune the branch to reduce computation.
        '''
        try:
            def maxlevel(gameState, depth, alpha, beta):
                cur_depth = depth + 1
                if gameState.isWin() or gameState.isLose() or cur_depth == self.depth:
                    return self.evaluationFunction(gameState)
                actions = gameState.getLegalActions(0)
                alpha1 = alpha
                maxvalue = -float('inf')
                for action in actions:
                    NextState = gameState.getNextState(0, action)
                    maxvalue = max(maxvalue, minlevel(NextState, cur_depth, alpha1, beta, 1))
                    if maxvalue > beta:
                        return maxvalue
                    alpha1 = max(alpha1, maxvalue)
                return maxvalue

            def minlevel(gameState, depth, alpha, beta, agentIndex):
                if gameState.isWin() or gameState.isLose():
                    return self.evaluationFunction(gameState)
                actions = gameState.getLegalActions(agentIndex)
                beta1 = beta
                minvalue = float('inf')
                for action in actions:
                    NextState = gameState.getNextState(agentIndex, action)
                    if agentIndex == gameState.getNumAgents()-1:
                        minvalue = min(minvalue, maxlevel(NextState, depth, alpha, beta1))
                    else:
                        minvalue = min(minvalue, minlevel(NextState, depth, alpha, beta1, agentIndex+1))
                    if minvalue < alpha:
                        return minvalue
                    beta1 = min(beta1, minvalue)
                return minvalue

            actions = gameState.getLegalActions(0)
            alpha = -float('inf')
            beta = float('inf')
            scores = []
            for action in actions:
                NextState = gameState.getNextState(0, action)
                score = minlevel(NextState, 0, alpha, beta, 1)
                alpha = max(alpha, score)
                scores.append(score)

            highscore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == highscore]
            chosenIndex = random.choice(bestIndices)

            return actions[chosenIndex]

        except:
            raise NotImplementedError("To be implemented")
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        '''
        The above methods are assuming the adversaries always choose the best actions.
        However, it may always contrast to the real world.
        Therefore, we deal with this situation by using expect value to replace the
        minvalue which can be closer to the reality situation.
        We calculate the expect value of all the outcomes from the possible actions
        in explevel.
        '''
        try:
            def maxlevel(gameState, depth):
                cur_depth = depth + 1
                if gameState.isWin() or gameState.isLose() or cur_depth == self.depth:
                    return self.evaluationFunction(gameState)
                actions = gameState.getLegalActions(0)
                maxvalue = -float('inf')
                for action in actions:
                    NextState = gameState.getNextState(0, action)
                    maxvalue = max(maxvalue, explevel(NextState, cur_depth, 1))

                return maxvalue

            def explevel(gameState, depth, agentIndex):
                if gameState.isWin() or gameState.isLose():
                    return self.evaluationFunction(gameState)
                actions = gameState.getLegalActions(agentIndex)
                expvalue = 0
                for action in actions:
                    NextState = gameState.getNextState(agentIndex, action)
                    if agentIndex == gameState.getNumAgents()-1:
                        expvalue += maxlevel(NextState, depth)
                    else:
                        expvalue += explevel(NextState, depth, agentIndex+1)
                
                if len(actions) == 0:
                    return 0
                expvalue /= len(actions)
                return expvalue

            actions = gameState.getLegalActions(0)
            scores = []

            for action in actions:
                NextState = gameState.getNextState(0, action)
                score = explevel(NextState, 0, 1)
                scores.append(score)

            highscore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == highscore]
            chosenIndex = random.choice(bestIndices)

            return actions[chosenIndex]

        except:
            raise NotImplementedError("To be implemented")
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    
    # Begin your code (Part 4)
    '''
    This part I will explain in the report.
    '''
    try:

        newPos = currentGameState.getPacmanPosition()
        NewFood = currentGameState.getFood()
        NewCapsule = currentGameState.getCapsules()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newFoodsDistances = [manhattanDistance(newPos, food) for food in NewFood.asList()]
        ScaredGhostStates = [ghostState for ghostState in newGhostStates if ghostState.scaredTimer > 0]
        UnscaredGhostStates = [ghostState for ghostState in newGhostStates if ghostState.scaredTimer == 0]

        score = 0
        totalFood = currentGameState.getNumFood()
        currentFood = 1 if not newFoodsDistances else len(newFoodsDistances)
        minScaredGhostDistance = 0 if not ScaredGhostStates \
        else min([manhattanDistance(newPos, state.getPosition()) for state in ScaredGhostStates])

        minGhostDistance = 0 if not UnscaredGhostStates \
        else min([manhattanDistance(newPos, state.getPosition()) for state in UnscaredGhostStates])

        minCapsuleDistance = 0 if not NewCapsule else min([manhattanDistance(newPos, state)for state in NewCapsule])
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        decisions = len(currentGameState.getLegalActions(0))
        sumScaredTime = sum(newScaredTimes)
        weight = (totalFood/currentFood)**(0.5)

        if sumScaredTime > 0:
            if sumScaredTime > minScaredGhostDistance:
                score += (-5)*minScaredGhostDistance + currentGameState.getScore() + 100*len(NewCapsule)
            else:
                score += currentGameState.getScore() + 0.5*minGhostDistance + (-1)*minCapsuleDistance
                score += (-1)*newNearestFoodDistance*weight
        else:
            
            score += currentGameState.getScore() + 0.5*minGhostDistance
            score += (-1)*newNearestFoodDistance*weight + (-100)*len(NewCapsule) + (-1)*minCapsuleDistance
    
        return score

    except:
        raise NotImplementedError("To be implemented")
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
