// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = (LENGTH + 1) *'z';

// Hash table
int total_words = 0;
node *table[N];

// Returns true if word is in dictionary else false ***FOURTH
bool check(const char *word)
{
    int index = hash(word);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number ***SECOND
unsigned int hash(const char *word)
{
    int sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }

    return (sum % N);
}

// Loads dictionary into memory, returning true if successful else false ***FIRST
bool load(const char *dictionary)
{

    FILE *file = fopen(dictionary, "r");

    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);
        n->next = NULL;

        int index = hash(word);
        if (table[index] == NULL)
        {
            table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        total_words++;
    }

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded ***THIRD
unsigned int size(void)
{
    return total_words;
}

// Unloads dictionary from memory, returning true if successful else false ***FIFTH
bool unload(void)
{

    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = cursor;

        if (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }

    return true;
}
