import random
def spin_row():
    symbols=["❤️"  ,"7️⃣" , "🍒",  "🍋" , "🔔"]
    
    results=[]
    for symbol in range(3):
        results.append(random.choice(symbols))
    return results

def print_row(row):
    print("------------")
    print(" | ".join(row))
    print("------------")

def get_payout(row,bet):
    if row[0]==row[1]==row[2]:
        if row[0]=="🍒":
            return bet*3
        if row[0]=="❤️":
            return bet*5
        if row[0]=="🍋":
            return bet*2
        if row[0]=="🔔":
            return bet*10
        if row[0]=="7️⃣":
            return bet*20
    return 0

def main():
    balance=100
    print("welcome to slots")
    print("Symbols:❤️  7️⃣  🍒  🍋  🔔")
    while balance>0:
        print(f"current balance={balance}$")
        bet=input("enter the bet amount: ")
        if not bet.isdigit():
            print("please enter a valid number")
            continue
        bet=int(bet)
        if bet>balance:
            print("insufficent funds")
            continue
        if bet<=0:
            print("bet must be greater than 0")
            continue
        balance-=bet
        row=spin_row()
        print("spinning...\n")
        print_row(row)
        
        payout=get_payout(row,bet)
        if payout>0:
            print(f"you won {payout}$")
        else :
            print("sorry you lost")
        balance+=payout
        play_again=input("do u want to play again ? (Y/N) ")
        if play_again.upper()!="Y":
            break

if __name__=='__main__':
    main()
