#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

int main(void)
{

    string texto = get_string("Text: ");

    float sentences = 0;
    float words = 1;
    float letters = 0;
    string vazio = " ";

    for (int i = 0, n = strlen(texto); i < n; i++)
    {
        if (isspace(texto[i]))
        {
            words++;
        }

        if (texto[i] == '.' || texto[i] == '!' || texto[i] == '?')
        {
            sentences++;
        }

        if (isalpha(texto[i]))
        {
            letters++;
        }

    }

    float L = letters / words * 100;
    float S = sentences / words * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int resultado = round(index);

    if (resultado >= 1 && resultado <= 16)
    {
        printf("Grade %i\n", resultado);
    }
    else
    {
        if (resultado < 1)
        {
            printf("Before Grade 1\n");
        }
        if (resultado > 16)
        {
            printf("Grade 16+\n");
        }
    }
}