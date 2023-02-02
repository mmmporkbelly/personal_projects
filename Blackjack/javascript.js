//arrays for cards to find image, also an array to keep track of used cards
    let cardNum = [2,3,4,5,6,7,8,9,10,'j','q','k','a'];
    let cardSuit = ['c','d','h','s'];
    let usedCards = []; 

//arrays to store player and computer hands
    let playerHand = [];
    let computerHand = [];

//store value of hidden dealer  to reveal after stand or stay
    let hiddenCard = [];

//win counter
    let computerWins = 0;
    let playerWins = 0;

//button methods
    //new game button
    $('#new-game').on("click", function(){
        //reset arrays
        playerHand = [];
        computerHand = [];
        usedCards = [];

        //clear table
        let tempCard = addCard();
        playerHand.push(tempCard[0]);
        $('#player-row').html(`<td><img src = "./card_images/` + tempCard[0] + tempCard[1] + `.png"></image></td>`);
        tempCard = addCard();
        computerHand.push(tempCard[0]);
        $('#computer-row').html(`<td><img src = "./card_images/` + tempCard[0] + tempCard[1] + `.png"></image></td>`);
        tempCard = addCard();
        playerHand.push(tempCard[0]);
        $('#player-row').append(`<td><img src = "./card_images/` + tempCard[0] + tempCard[1] + `.png"></image></td>`);
        
        //add computer card but hide the image
        tempCard = addCard();
        hiddenCard = tempCard;
        computerHand.push(tempCard[0]);
        $('#computer-row').append(`<td id="hidden_Card"><image src = "./card_images/card_back.png"></image></td>`);
        
        //but if dealer has pocket blackjack, reveal hand, per wikipedia rules
        if(totalCardValue(computerHand)=='Blackjack!'){
            $('#hidden_Card').html(`<image src = "./card_images/` + hiddenCard[0] + hiddenCard[1] + `.png"></image></td>`)
        }
        
        //reset computer and human hand value lines
        $('#humanHandValue').text('Your hand value is '+ totalCardValue(playerHand) +'!');
        $('#compHandValue').text("It's your turn! Click hit to draw a card, or press stand if you are satisfied with your hand.");

        //enable hit and stand buttons, disable new game button
        $("#hit").prop('disabled', false);
        $("#stand").prop('disabled', false);
        $("#new-game").prop('disabled', true);

        //if player has blackjack warn player
        if(totalCardValue(playerHand)=="Blackjack!"){
            $('#humanHandValue').text("Woah! Blackjack! Don't press hit, press stand...");
            $("#hit").prop('disabled', true);
        }
    });
    
    //hit button
    $('#hit').on("click", function(){
        //add card values to player hand obj, add picture to player hand
        let tempCard = addCard();
        playerHand.push(tempCard[0]);
        $('#player-row').append(`<td><img src = "./card_images/` + tempCard[0] + tempCard[1] + `.png"></image></td>`);
        
        //check total value of player's hand, update on page. 
        let handValue = totalCardValue(playerHand);
        $('#humanHandValue').text('Your hand value is '+handValue +'!');

        //if bust, stop game by disabling stand and hit buttons. enable new game button
        if(handValue=='bust'){
            $('#humanHandValue').text('You bust! You lose, click new game to play again!');
            computerWins++;
            $('#compHandValue').text("You lost... Click new game to play again!");
            $('#win-counter').text(`Computer wins = `+ computerWins +` Player wins = ` + playerWins);
            $("#hit").prop('disabled', true);
            $("#stand").prop('disabled', true);
            $("#new-game").prop('disabled', false);
        }
    });

    //stand or stay button
    $('#stand').on("click", function(){
        //add cards to dealer's hand while hand total is under 17, per blackjacks rules on wikipedia
        while(totalCardValue(computerHand)<17){
            tempCard = addCard();
            computerHand.push(tempCard[0]);
            $('#computer-row').append(`<td><img src = "./card_images/` + tempCard[0] + tempCard[1] + `.png"></image></td>`);
        }

        //reveal dealer hand
        $('#hidden_Card').html(`<image src = "./card_images/` + hiddenCard[0] + hiddenCard[1] + `.png"></image></td>`)
        
        //disable hit and stand buttons, enable new game button
        $("#hit").prop('disabled', true);
        $("#stand").prop('disabled', true);
        $("#new-game").prop('disabled', false);

        //check if dealer busted hand
        if(totalCardValue(computerHand)=='bust'){
            $('#compHandValue').text("Dealer's hand is a bust. Yay, you won! Click new game to play again!");
            playerWins++;
        }
        //if not, compare hand values. first tie, then if one of the players get blackjack, and then literal card values
        else if(totalCardValue(computerHand)==totalCardValue(playerHand)){
            $('#compHandValue').text("Dealer's hand value is "+totalCardValue(computerHand) +"! You tied! Click new game to play again!");
        }
        else if(totalCardValue(computerHand)=='Blackjack!'){
            $('#compHandValue').text("Dealer got a blackjack! Too bad, you lost. Click new game to play again!");
            computerWins++;
        }
        else if(totalCardValue(playerHand)=='Blackjack!'){
            $('#compHandValue').text("Dealer's hand value is "+totalCardValue(computerHand) +"! You got a blackjack, so you won! Click new game to play again!");
            playerWins++;
        }
        else if(totalCardValue(playerHand)>totalCardValue(computerHand)){
            $('#compHandValue').text("Dealer's hand value is "+totalCardValue(computerHand) +"! You won! Click new game to play again!");
            playerWins++;
        }
        else{
            $('#compHandValue').text("Dealer's hand value is "+totalCardValue(computerHand) +"! You lost... Click new game to play again!");
            computerWins++;
        }

        //update win counter
        $('#win-counter').text(`Computer wins = `+ computerWins +` Player wins = ` + playerWins);
    });
    
//functions
    //add card function
    let addCard = () => {
        //Check card w/ recursive function to usedCards to see if it's an unused card
        let num = cardNum[Math.floor(Math.random()*cardNum.length)];
        let suit = cardSuit[Math.floor(Math.random()*cardSuit.length)];
        if(usedCards.includes(num+suit)){
            return addCard();
        }
       
        //add new card to usedCard to keep track of used cards, return array of new card value and suit
        usedCards.push(num+suit);
        return [num, suit];
    }
    
    //adds card values of hand, returns number, 'bust', or 'blackjack'
    let totalCardValue = arrayHand =>{
        let totalCount=0;
        let aceCount=0;

        //adds all values in hand minus ace
        arrayHand.forEach(function(element){
            if(['j','q','k'].includes(element)){
                totalCount = totalCount + 10;
            }
            else if (element == 'a'){
                aceCount++;
            }
            else{
                totalCount+=Number(element);
            }
            console.log(totalCount);
        })

        //add ace values to hand, account for multiple aces
        for (let i = 0; i<aceCount; i++){
            if(totalCount>10){
                totalCount++;
            }
            else if(totalCount==10 && aceCount>1){
                totalCount++;
            }
            else if(totalCount==9 && aceCount>2){
                totalCount++;
            }
            else if(totalCount==8 && aceCount>3){
                totalCount++;
            }
            else{
                totalCount+=11;
            }
        }

        //check if blackjack
        console.log(totalCount);
        if(arrayHand.length == 2 && totalCount==21){
            return 'Blackjack!';
        }
        else if (totalCount>21){
            return 'bust';
        }
        else{
            return totalCount;
        }
    }