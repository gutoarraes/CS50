#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Check if there is only command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key");
        return 1;
    }

    // Check if command line argument is only made of digits 
    int size_argument = strlen(argv[1]);
    for (int z = 0; z < size_argument ; z++)
    {
        if (!isdigit(argv[1][z]))
        {
            printf("Usage: ./caesar key");
            return 1;
        }
    }
    
    //transpose argument into an integer
    int k = atoi(argv[1]);

    //check if command line argument is positive or neutral
    for (int i = 0; i < k ; i++)
    {
        if (k < 0)
        {
            printf("Fail\n");
            return 1;
        }
        else
        {
            string plaintext = get_string("plaintext:");

            //cipher the text provided in the variable "plaintext" submitted by the user
            printf("ciphertext: ");
            for (int y = 0; y < strlen(plaintext); y++)
            {
                if (islower(plaintext[y]))
                {
                    printf("%c", ((plaintext[y] - 97 + k) % 26) + 97);
                }
                else if (isupper(plaintext[y]))
                {
                    printf("%c", ((plaintext[y] - 65 + k) % 26) + 65);
                }
                else
                {
                    printf("%c", plaintext[y]);
                }
            }
            printf("\n");
        }
        return 0;

    }

}

