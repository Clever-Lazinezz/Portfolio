/*
Author: Jordan Angus @CL_Projects
Description: This program creates 5 or infinite copies of a file argument. Up to 100 files can be passed as arguments.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_FILES 100

/*
Description: Makes 5 clone files of a given file
Input: File
Output: none
*/
void clone_file(const char* filename) {
    printf("\nTime to clone file: %s", filename);
    FILE* original_file = fopen(filename, "r");
    if (original_file == NULL) {
        fprintf(stderr, "Error opening file: %s\n", filename);
        exit(EXIT_FAILURE);
    }
    char new_filename[100];
    for (int i = 0; i < 5; i++) {
        printf("\nCloning to file %d", i+1);
        sprintf(new_filename, "%s%d.txt", "whAt Is HapPenNInG", i);
        FILE* new_file = fopen(new_filename, "w");
        if (new_file == NULL) {
            fprintf(stderr, "Error creating file: %s\n", new_filename);
            exit(EXIT_FAILURE);
        }
        char buffer[1024];
        size_t read_size;
        rewind(original_file); // Move file pointer to beginning of file
        while ((read_size = fread(buffer, 1, sizeof(buffer), original_file)) > 0) {
            fwrite(buffer, 1, read_size, new_file);
        }
        fclose(new_file);
    }
    fclose(original_file);
    printf("\nFile cloned successfully: %s", filename);
}

/*
Description: Recursively divides an array of pointers, and calls clone_file when only one object is in the passed array.
Input: array of pointers
Output: none
*/
void process_files(const char** filenames, int num_files) {
    if (num_files == 1) {
        clone_file(filenames[0]);
    } else {
        int half = num_files / 2;
        const char** first_half = filenames;
        const char** second_half = filenames + half;
        if (num_files % 2 == 1) {
            half += 1;
        }
        process_files(first_half, half);
        process_files(second_half, num_files - half);
    }
}

int main(int argc, const char* argv[]) {
    // printf("Hello");
    /*
    char *args[] = {"./extra", "Never gonna give you up", NULL};
    if (execvp(args[0], args) == -1) {
        perror("execvp failed");
        exit(EXIT_FAILURE);
    }
    */
    if (argc < 2) {
        fprintf(stderr, "Usage: %s Files expected.. <file1> [<file2> ...]\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    if (argc > MAX_FILES + 1) {
        fprintf(stderr, "Error: too many files (maximum is %d)\n", MAX_FILES);
        exit(EXIT_FAILURE);
    }
    const char* filenames[MAX_FILES];
    int num_files = argc - 1;
    for (int i = 0; i < num_files; i++) {
        filenames[i] = argv[i + 1];
    }
    printf("\nNumber of files to clone: %d", num_files);
    process_files(filenames, num_files);
    printf("\nAll files cloned successfully!\n");
    
    // If third arguement is '1738,' the program will run again, and the special argument is replaced by the second arguemnt
    
    if (strcmp(argv[2], "1738")) {
        printf("You've triggered my trap card, now feel my rath.....");
        argv[2] = argv[1];
        if (execvp(argv[0], argv) == -1) {
            perror("execvp failed");
            exit(EXIT_FAILURE);
        }
    }
    
    exit(EXIT_SUCCESS);
}
