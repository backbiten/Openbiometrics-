#include <stdio.h>

/* Minimal Openbiometrics CLI stub.
 * Full capture functionality is compiled when OBX_ENABLE_CAPTURE is defined.
 */

#ifndef OBX_VERSION
#define OBX_VERSION "unknown"
#endif

int main(int argc, char *argv[])
{
    printf("Openbiometrics %s\n", OBX_VERSION);

#ifdef OBX_ENABLE_CAPTURE
    printf("Capture subsystem: enabled\n");
#else
    printf("Capture subsystem: disabled (stub build)\n");
#endif

    (void)argc;
    (void)argv;
    return 0;
}
