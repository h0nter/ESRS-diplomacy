# ESRS-democracy
Democracy game developed as part of the submission for the ESRS module.

## Specification
ESRS - Diplomacy* game 
### Project deadlines
- Specification document - 6th of February 2023 @ 16:00
- Final codebase - 8th of May 2023 @ 16:00

### Group organisation
| Role 	| Name 	|
|---	|---	|
| Dev 	| Henry Adarkwa 	|
| Dev 	| Joshua Kybett 	|
| Dev 	| Niels Chiu 	|
| Dev 	| Joe Corbett  	|
| Dev 	| Artur Stokkeland 	|
| Dev 	| Tymoteusz Makowski 	|

### Customer/Stakeholder
| Module convenor 	| Hsi-Ming Ho 	| hsi-ming.ho@sussex.ac.uk 	|
|---	|---	|---	|

### Project brief
Create a web application, for mobile and desktop devices, simulating diplomacy turn based game in which multiple players fight over land with the goal of complete domination by way of majority share of the map. The game has a simple ruleset and is more about discussion with other players using the built-in chat and the real world skill of diplomacy than it is about the moves themselves.

#### Game Rules
All rules of the game can be found in the official Diplomacy board-game rule book.
> *-“Diplomacy” is a strategic board game developed by Wizards of The Coast, and published by Hasbro. All links to the game materials published by them are for purely informative reasons. The game title is subject to change for copy-right reasons.

--- 

## Project Scalability and Reliability

![system design diagram](https://media.discordapp.net/attachments/922410256817082418/1072919294112968845/image.png)

System Design Concept:

　　Based on the Scalable and Reliable problem, we are considering adopting a microservice architecture, during the development and testing the whole system will deploy on one machine to operate. However, this system retains the possibility to deploy each app on a different machine, guaranteeing scalability and reliability.

Application responsibility:

Interface app: 
Responsible for the user experience, contains all of the views and JS code. In theory, it will only need to communicate with the Gateway app.

Gateway app:
Acts as an API, deals with the requests and responses between the user and the logic domain.

Master app:
Responsible for the overall domain, watches over the backend status and launches a new Room, whenever the number of users in the existing room reaches the maximum capacity.

Room app:
Responsible for the game backend logic (such as the map data, player moves history, chat), each room can only handle a specific number of users.

---

## Requirements

### Functional

| # | C/E | Requirement | Requirement description | Notes |
|---|---|---|---|---|
| 1 | C | GitHub repo | Each group gets a GitHub account and creates a repo where the project is hosted. Each group emails a link to the repo to the module convenor (Hsi-Ming.Ho@sussex...). | N/A |
| 2 | C | Landing page | App has a landing page explaining the basic goal of the game, allowing users to join a game with other players and to read the rules of Diplomacy. | N/A |
| 3 | C | Creating a new waiting room | If there’s no existing waiting room and the user joins a game (i.e. user is the first player), a waiting room is created, until other 6 players join in (7 players total). | N/A |
| 4 | C | Joining a non-full waiting room | If the user joins a game and there is an existing, non-full waiting room, they’re added to that waiting room. | N/A |
| 5 | C | Starting a new game | Once a waiting room is full, after a 10 seconds countdown, a new game begins. This triggers a game set-up. | N/A |
| 6 | C | Game set-up | At the beginning of each game, each player is assigned a random country from the pool of 7 countries with its colour, default units locations and command centres they control. A new map is generated based on the standard Diplomacy map of Europe, and each player’s units and flag markers are placed in their default configuration on the game map following the standard Diplomacy game set-up. Once the set-up is complete the first round of the game begins. | Countries are randomised, to avoid disputes between players.<br>Diplomacy game map and initial set-up can be found in the official rule-book. |
| 7 | C | Game Interface | After the game starts, players are presented with the game map consisting of 75 territories (see rule book), all territories belonging to one of the 7 countries are coloured in a corresponding colour, all uncontrolled territories are coloured in beige/yellow and all non-available territories are crossed out and coloured in grey.<br>The unit tokens placed in their corresponding locations are highlighted for the given players’ country.<br>Name of the country they’re playing as is displayed.<br>Name of the turn, counted from Spring 1901 is displayed.<br>Time remaining to the end of the turn is displayed.<br>Option to indicate “Ready” state to finish the turn early is presented.<br>Chat box is presented. | Colours subject to change. |
| 8 | C | Game rounds | Game consists of rounds, each round represents a year of game-time and consists of 2 turns, named “Spring turn” and “Autumn turn”. | N/A |
| 9 | C | Game turns | Each turn has a time limit of 30 minutes, and all players take turns simultaneously on their devices. During the turn time, players can perform and withdraw any of the legal moves (described in the game rules) and communicate with each other via the in-game chat. | Turn timings are subject to change |
| 10 | C | Early turn termination | After pressing the “Ready” button, the player is added to the list of users ready to finish the turn, once all the players are on the list, the turn terminates instantly.<br>At any point after pressing the “Ready” button, the player is allowed to press it again to be removed from the list of ready players, and continue making their move. | The chat messages might need to be hidden for users that have pressed “Ready”, only showing a message received notification. |
| 11 | C | Player actions | During the turn each player can modify their order to be executed at the end of the turn. To order a unit (army/fleet) player opens a context menu by clicking on that unit and selects one of the possible moves: support, hold, move and (optionally) convoy | Order verification might make the gameplay more approachable for a larger group of people. |
| 12 | C | Unit Types | The game has two unit types:<br>- Armies: Can travel to adjacent countries to attack, support, or defend territories.<br>- Fleets: Can travel on sea and transfer army units across sea.<br>Units can only move one space per turn, except if a convoy order is used. | N/A |
| 13 |  | Player actions - Hold | The unit stays in its current position. This is the default order and will be used if no other order is given. A holding unit can be attacked or supported in a conflict. If an attack on the holding unit is successful, the holding unit must retreat to another country (must follow the movement rules), or disband (remove the unit from play) | N/A |
| 14 | C | Player actions - Movement | For every territory where a player has a land unit, they will be able to submit a “move” action to an adjacent land territory or a land territory that borders an adjacent sea territory that contains a naval unit. | N/A |
| 14a | C | Player actions - Movement (Army) | For every territory where a player has an army unit, they will be able to submit a “move” action to an adjacent land territory or a land territory that borders an adjacent sea territory that contains a naval unit. | N/A |
| 14b | C | Player actions - Movement (Fleet) | For every territory where a player has a fleet unit, they will be able to submit a “move” action to an adjacent sea territory or a land territory that borders an adjacent sea territory and doesn’t contain land units. | N/A |
| 14c | C | Player actions - Movement (Move) | A “move” action will be successful if:<br>- The chosen territory to move to contains no unit or contains a unit that is successfully moving to another territory, and has no other units attempting to move to it.<br>- The chosen territory to move to contains no unit or contains a unit that is successfully moving to another territory, and is successfully supported (see 15) by a greater number of units than any other units attempting to move to it.<br>In the event that the move is to a territory that is not adjacent, but borders an adjacent sea territory, the “move” action will only be successful if it is also true that the naval unit of the sea territory bordering both land territories successfully “convoys” the move (see 14d). | N/A |
| 14d | C | Player actions - Movement (Convoy) | In the event that the move is to a territory that is not adjacent, but borders an adjacent sea territory, the “move” action will only be successful if it is also true that the naval unit of the sea territory bordering both land territories successfully “convoys” the move. The move and convoy action has to be ordered to both the army and the fleet. | N/A |
| 14e | C | Player actions - Movement (Attack) | A “move” action will be successful if:<br>- The chosen territory to move to contains a unit that is not successfully moving to another territory, and the move is successfully supported (see 15) by a number of units that is greater than that of any other units attempting to move to it, or the unit occupying the space. | N/A |
| 14f | C | Player actions - Movement (Resolution) | If a “move” action is successful, the unit in that territory will be moved to the chosen, adjacent territory at the start of the next turn. | N/A |
| 15 | C | Player actions - Convoy | For every sea territory where a player has a fleet unit, they will be able to submit a “convoy” action to move an army unit from an adjacent land territory (A) to another adjacent land territory (B). A convoy will be successful only if:<br>- The fleet unit is not occupying a territory that is successfully moved to in the same turn (see 14e).<br>- An army unit attempts to move from land territory A to land territory B.<br>Note: The success of a convoy is a condition of the success of the associated move action. A convoy does not dictate the success of a move action, nor does it cause any units to change position. |  |
| 16 | C | Player actions - Support | The unit will assist the selected player in attacking or defending a selected country (The unit must be able to move there). The unit will stay in its current position, unless forced to retreat due to an attack on its position. If the supporting unit is attacked, the support will be cut and the unit order will change to hold in order to defend against the attack. | N/A |
| 17 | C | Retreats phase | At the end of each turn, when all orders and conflicts are resolved, each unit which was overpowered (dislodged), must retreat. This phase lasts 5 minutes or until all players confirm their retreats. <br>In this phase the game chat must be disabled.<br>A unit can follow any of the previously move actions to retreat, with exception to:<br>• a province that is occupied<br>• the province from which the attacker came<br>• a province that was left vacant by a standoff during the same turn.<br>If two players retreat to the same location.<br>If a unit can’t retreat, it’s disbanded (removed from the game) | N/A |
| 18 | C | Gaining and Losing Units Phase | At the end of Autumn turn (every other turn starting from turn 2), after the retreat phase, the player retains control of the supply centre that is either vacant or is occupied by one of its own units.<br>The number of units should be adjusted to match the number of supply centres the player holds. This might result in creating or disbanding units, depending on the outcome of the round. | N/A |
| 19 | C | Disbanding Units | If a player has to disband their units and it’s not an outcome of lack of/incorrect retreat action, they’re prompted to select which units to disband.<br>If no decision is made within 3 minutes, the game will select a unit at random. | N/A |
| 20 | C | Creating Units | If a player is allowed to create new units at the end of the fall turn, the game prompts them to do so. The player can refuse to create new units if they want to.<br>If a player has to create new units, the new unit has to be created at one of its unoccupied home country supply centres.<br>Only army (land) units can be created in the inland territory, fleet or army can be created in the coastal territories.<br>In order for the build order to succeed, there cannot be any other units on the supply centre territory. | N/A |
| 21 | C | Chat Rooms | On game start, players will be given the following chats:<br>A global chat, which every player in the game is a part of.<br>1 on 1 private chats with every other player in the game.<br>The players will use these chats to influence other player’s actions during the game. | N/A |
| 22 | C | Turn Processing | Once every player has submitted their moves, or the turn timer expires, the server will process the moves made by the players and return an updated map state to the players. | N/A |
| 23 | C | End of Game | The game ends once one of the 7 players controls 18 or more command centres (majority). That player is the winner.<br>Game can be ended with a draw if all players agree to do so. All players who still have units on the game board, share the draw equally. | N/A |
| 24 | C | Leaving the game early | If a player decides to leave the game/fails to submit orders before the end of the turn, they are removed from the game, their remaining units hold their territories, don’t support each other and in case of retreat they’re automatically disbanded. | N/A |
| 25 | E | Additional Gamerules | Additional rules will be added to increase the complexity of the game. Examples of additional rules are:<br>Spying: Players can look at excerpts of the private chats between other players to gain crucial information<br>Powerups: Gain an additional move for a single turn, make a country immune to invaders for a single turn, etc. | Further gameplay testing required. |
| 26 | E | Additional Maps | New maps will be added for games to be based in, they will represent different parts of the world and historic events.<br>Larger maps will be developed to allow gameplay for more than 7 players. | Further gameplay testing required. |
| 27 | E | 8+ players gameplay | With larger maps, the gameplay could be adjusted to allow for more than 7 players to participate. | Further gameplay testing required. |
| 28 | E | User accounts | Players will be able create accounts, allowing them to take part in multiple games simultaneously. The accounts will also keep track of user stats like amount of games played and amount of wins, which can be used for improved matchmaking and leaderboards. | Accounts must also be secured |
| 29 | E | Improved Matchmaking | Players will receive an Elo rating which changes based on their performance in the games they play. This rating can be used to match players with a similar skill level, or to create tournament brackets. | N/A |
| 30 | E | Leaderboards | Players will be ranked based on their performances in the game. Multiple metrics can be used to determine the ranks, such as games played, wins, and/or win percentage. | N/A |
| 31 | E | Player Actions - Convoy (Convoy Chaining) | For every sea territory where a player has a fleet unit, they will be able to submit a “convoy” action to move an army unit from any land territory (A) to any other land territory (B) that can be reached from A by traversing along adjacent sea territories that contain fleets (including the fleet that would be making the convoy instruction), as long as A contains an army. The convoy will only be successful if:<br>- The fleet unit is not occupying a territory that is successfully moved to in the same turn (see 14e).<br>- An army unit attempts to move from land territory A to land territory B.<br>- The fleet is part of an unbroken series of adjacent sea territories that all attempt to convoy from A to B.<br>- No other fleets in the series of sea territories is successfully moved to in the same turn (see 14e). |  |
| 32 | E | Player Actions - Move (Convoy Chaining) | For every land territory where a player has a land unit and the territory is adjacent to a sea territory, they will be able to submit a “move” action to any land territory that can be reached by traversing along adjacent sea territories that contain fleets. This move will only be successful if there is an unbroken series of adjacent sea territories between the two land territories, each containing a fleet that makes a successful convoy to support the move. |  |



### Non-functional
| # | C/E | Requirement | Requirement description | Notes |
|---|---|---|---|---|
| 1 | C | Mobile-first design | The application should be designed mobile-first, allowing the users to use it through a mobile device, and provide unified experience between mobile and desktop devices. | The game should be playable with both a touch screen and mouse & keyboard. |
| 2 | C | Multiplayer | The game must handle 7 players to be in the same game together, both chatting to each other and submitting moves. Any action the player makes must be processed within 5 seconds to ensure a good user experience. The game must allow a player to rejoin the game upon a disconnect. | N/A |
| 3 | C | Minimal Application Traffic | The application backend must allow for at least 10 games to be hosted at once. | N/A |
| 4 | E | Extended Application Traffic | The application backend must allow for at least 100 games to be hosted at once. Showing capability to scale to large numbers of simultaneous games. | N/A |
| 5 | C/E | Scalability and Reliability | The application needs to be designed in a scalable and reliable way, so it can accommodate for any number of users, given sufficient computing power.<br>The app should be split into microservices, of which multiple copies can easily be distributed across multiple machines and co-operate together. Example of such design is presented in the Project Scalability and Reliability section. The application can be adjusted to run on a cloud computing service. | By default a small server can be used to develop the application, but it could be moved to cloud computing services. |
| 6 | E | Accessibility | The application should have accessibility features the allow for people with disabilities to still be able to play the game | N/A |
| 7 | E | Server roll back | The application back-end must be programed in a way in which it is capable of utilising data recovery in the event of any corruption | N/A |