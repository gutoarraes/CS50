#include <stdio.h>
#include <cs50.h>

int height;

int main(void)
{


    while (height < 1 || height >= 8)
    {
        height = get_int("Please select a number between 1 and 8: ");
    }

    //build pyramid
    for (int i = height; i >= 1; i--)
    {
        //add spaces
        for (int space = 1; space < i; space++)
        {

            printf(" ");

        }

        //add hashtags
        for (int hash = height; hash >= i; hash--)
        {

            printf("#");
        }


        printf("\n");
    }

}