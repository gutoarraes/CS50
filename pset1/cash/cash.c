#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{

float change = -1;
int coins = 0;

while(change < 0)

    {
    change = get_float("How much change is needed?");
    }

    int cash = round(change * 100);

    if(cash >= 25)
    {
        cash -= 25;
        coins += 1;
    }
    if(cash >= 10)
    {
        cash -= 10;
        coins += 1;
    }
    if(cash >= 5)
    {
        cash -= 5;
        coins += 1;
    }
    else
    {
        cash -= 1;
        coins += 1;
    }
    printf("%i", coins);
}