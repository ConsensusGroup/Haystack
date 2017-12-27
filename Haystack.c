#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

void runTangleCommunication(void);
void setupUserAddress(char **userInformation);
void runHaystackInterface(void);
void checkMail(void);
void sendMail(void);
void printUserOptions(void);
char* findRecipientAddress(char* name);
//-----------------------------------------------------------------------------------------
// IVE FORGOTTEN TO CLOSE ALL THE FILES
//-----------------------------------------------------------------------------------------
#define MAX_LENGTH 100
char* UserSeed;
char* UserAddress;
char* UserName;

// Remember that I have to change this for threading
int main(int argc, char **argv) {
    
    setupUserAddress(argv);
    runHaystackInterface();
    
    return EXIT_SUCCESS;
}

//-----------------------------------------------------------------------------------------
//
//-----------------------------------------------------------------------------------------

void runTangleCommunication(void)
{
    // Syscall here on a seperate thread
}

void setupUserAddress(char **userInformation)
{
    UserSeed = malloc(sizeof(char)*MAX_LENGTH);
    UserAddress = malloc(sizeof(char)*MAX_LENGTH);
    UserName = malloc(sizeof(char)*MAX_LENGTH);
    FILE * userContactDetailsFile;
    char userContactDetailsBuffer[255];
    
    userContactDetailsFile = fopen("/home/robert/Desktop/Haystack/MyHaystack", "r");
    if(userContactDetailsFile == NULL) {
        printf("PROBLEM!\n");
        printf("Error %d \n", errno);
    }
    
    fscanf(userContactDetailsFile, "%s", userContactDetailsBuffer);
    int counter = 0;
    while(userContactDetailsBuffer[counter] != 0) {
        counter++;
    }
    userContactDetailsBuffer[counter] = '\n';
    userContactDetailsBuffer[counter+1] = 0;
    printf("\nMy Seed : %s\n", userContactDetailsBuffer );
    userContactDetailsBuffer[counter] = 0;
    strncpy(UserSeed, userContactDetailsBuffer, counter);
    
    counter = 0;
    fscanf(userContactDetailsFile, "%s", userContactDetailsBuffer);
    while(userContactDetailsBuffer[counter] != 0) {
        counter++;
    }
    userContactDetailsBuffer[counter] = '\n';
    userContactDetailsBuffer[counter+1] = 0;
    printf("My Address : %s\n", userContactDetailsBuffer );
    userContactDetailsBuffer[counter] = 0;
    strncpy(UserAddress, userContactDetailsBuffer, counter);
    
    counter = 0;
    fscanf(userContactDetailsFile, "%s", userContactDetailsBuffer);
    while(userContactDetailsBuffer[counter] != 0) {
        counter++;
    }
    userContactDetailsBuffer[counter] = '\n';
    userContactDetailsBuffer[counter+1] = 0;
    printf("My Name : %s\n", userContactDetailsBuffer );
    userContactDetailsBuffer[counter] = 0;
    strncpy(UserName, userContactDetailsBuffer, counter);
}

void runHaystackInterface()
{
    int userOption = -1;
    
    while(userOption != 3)
    {
        printUserOptions();
        
        scanf("%d", &userOption);
        if(userOption ==1)
        {
            checkMail();
        }
        else if(userOption ==2)
        {
            sendMail();
        }
        else
        {
            break;
        }
    }
}

void checkMail(void)
{
    // Syscall to update latest mail in message
    
    // Read the file
    
    printf("Pretend mail here\n");
}

char* findRecipientAddress(char* name)
{
    char* address = NULL;
    FILE * userContactDetailsFile;
    char userContactDetailsBuffer[255];
    
    userContactDetailsFile = fopen("/home/robert/Desktop/Haystack/HaystackContacts", "r");
    if(userContactDetailsFile == NULL) {
        printf("PROBLEM!\n");
    }

    int contactFound = 0;
    while(!contactFound)
    {
        fscanf(userContactDetailsFile, "%s", userContactDetailsBuffer);
        int counter = 0;
        while(userContactDetailsBuffer[counter] != 0) {
            counter++;
        }
        userContactDetailsBuffer[counter] = '\n';
        userContactDetailsBuffer[counter+1] = 0;
        //printf("2 : %s\n", userContactDetailsBuffer );
        userContactDetailsBuffer[counter] = 0;
        if(strcmp(name, userContactDetailsBuffer) == 0)
        {
            printf("\nFound The Contact!\n\n");
            contactFound = 1;
            fscanf(userContactDetailsFile, "%s", userContactDetailsBuffer);
            int counter = 0;
            while(userContactDetailsBuffer[counter] != 0) {
                counter++;
            }
            //printf("Counter = %d\n", counter);
            userContactDetailsBuffer[counter] = '\n';
            userContactDetailsBuffer[counter+1] = 0;
            //printf("3 : %s\n", userContactDetailsBuffer );
            address = malloc(sizeof(char)*counter+1);
            strncpy(address, userContactDetailsBuffer, counter);
        }
        // Skip past this
        fscanf(userContactDetailsFile, "%s", userContactDetailsBuffer);
    }
    return address;
}

void sendMail(void)
{
    char recipient[100];
    char message[100];
    
    printf("\nWho is the recipient?\n");
    scanf("%s", recipient);
    printf("<Mail will be going to %s>\n", recipient);
    
    // NULL FINISH RECIPIENT
    int counter = 0;
    while(recipient[counter] != 0) {
        counter++;
    }
    recipient[counter] = 0;
    findRecipientAddress(recipient);
    
    printf("What is the message?\n");
    char c;
    while ((c = getchar()) != '\n' && c != EOF) { }
    
    char *line = NULL;
    size_t size;
    if (getline(&line, &size, stdin) == -1) {
        printf("No line\n");
    } else {
        printf("%s\n", line);
    }
 
    // Write message to a file
    FILE * messageFile = fopen("/home/robert/Desktop/Haystack/messageFile", "w");
    if(messageFile == NULL) {
        printf("PROBLEM!\n");
        printf("Error %d \n", errno);
    }
    fprintf(messageFile, "%s", line);
    fclose(messageFile);
    
    // Create syscall command
    char *command = malloc(400);
    strcpy(command, "ccr -e -r ");
    strcat(command, recipient);
    strcat(command, " < messageFile > encodedMessage");
    strcat(command, "\0");

    printf("The command string will be (%s)\n" ,command);

    // Syscall to encode file
    system(command); // CHANGE THIS
    
    // Read the encoded message file
    printf("**********************************************************************\n");
    char *encodedMessageBuffer = malloc(4096);
    int ch;
    int fileCounter = 0;
    FILE *encodedFile;
    encodedFile = fopen("/home/robert/Desktop/Haystack/encodedMessage", "r");
    if (encodedFile) {
        while ((ch = getc(encodedFile)) != EOF) {
            encodedMessageBuffer[fileCounter++] = (char) ch;
            putchar(ch);
        }
        fclose(encodedFile);
    }
    encodedMessageBuffer[fileCounter++] = '\0';
    printf("**********************************************************************\n");
    printf("    Count - %d\n", fileCounter);
    printf("**********************************************************************\n");
    
    // Syscall here
    // syscall("python 'YourSendScriptName.py' 'Hello everyone' 'XWYSHSS'")
    printf("Sent\n");
    // Remove message file after all this is done
}

void printUserOptions(void)
{
    printf("\nChoose an option:\n");
    printf("1 - Check Latest Mail\n");
    printf("2 - Compose mail\n");
    printf("3 - Quit\n");
}