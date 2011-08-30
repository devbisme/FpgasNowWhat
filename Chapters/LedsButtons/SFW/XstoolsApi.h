// The following ifdef block is the standard way of creating macros which make exporting
// from a DLL simpler. All files within this DLL are compiled with the XSTOOLSAPI_EXPORTS
// symbol defined on the command line. this symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see
// TCM8240_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef XSTOOLSAPI_EXPORTS
#define XSTOOLSAPI __declspec( dllexport )
#else
#define XSTOOLSAPI __declspec( dllimport )
#endif

/// Open a channel to a HostIoToMemory module in the FPGA.
///\return A pointer to the channel.
extern "C" XSTOOLSAPI HostIoToMemory *XsMemInit(
    unsigned int xsusbInst,   ///< [in] XSUSB port instance (usually 0).
    unsigned int moduleId,    ///< [in] HostIo module identifier.
    unsigned int &rAddrWidth, ///< [out] Number of address bits.
    unsigned int &rDataWidth  ///< [out] Number of data bits.
    );

/// Send data to memory-like module in FPGA.
///\return 0 if operation was successful, non-zero if failure.
extern "C" XSTOOLSAPI int XsMemWrite(
    HostIoToMemory           *pHostIoModule, ///< [in] Pointer to HostIoToMemory module.
    unsigned int const       addr,           ///< [in] Starting address for writing to memory.
    unsigned long long const *pData,         ///< [in] Pointer to data elements destined for memory.
    unsigned int const       nData           ///< [in] Number of data elements to write.
    );

/// Get data from memory-like module in FPGA.
///\return 0 if operation was successful, non-zero if failure.
extern "C" XSTOOLSAPI int XsMemRead(
    HostIoToMemory            *pHostIoModule, ///< [in] Pointer to HostIoToMemory module.
    unsigned int const        addr,           ///< [in] Starting address for reading from memory.
    unsigned long long *const pData,          ///< [in] Pointer to storage for data elements from memory.
    unsigned int              nData           ///< [in] Number of data elements to read.
    );

/// Open a channel to a HostIoToDut module in the FPGA.
///\return A pointer to the channel.
extern "C" XSTOOLSAPI HostIoToDut *XsDutInit(
    unsigned int xsusbInst,   ///< [in] XSUSB port instance (usually 0).
    unsigned int moduleId,    ///< [in] HostIo module identifier.
    unsigned int &rNumInputs, ///<[out] Number of bits in input vector to DUT.
    unsigned int &rNumOutputs ///<[out] Number of bits in output vector of DUT.
    );

/// Send inputs to a DUT in the FPGA.
///\return 0 if operation was successful, non-zero if failure.
extern "C" XSTOOLSAPI int XsDutWrite(
    HostIoToDut                *pHostIoModule, ///< [in] Pointer to HostIoToDut module.
    unsigned char const *const pInputs,        ///< [in] Pointer to input vector values for DUT.
    unsigned int               numInputs       ///< [in] Number of inputs to force to given values.
    );

/// Get outputs from a DUT in the FPGA.
///\return 0 if operation was successful, non-zero if failure.
extern "C" XSTOOLSAPI int XsDutRead(
    HostIoToDut          *pHostIoModule, ///< [in] Pointer to HostIoToDut module.
    unsigned char *const pOutputs,       ///< [in] Pointer to output vector values from DUT.
    unsigned int         numOutputs      ///< [in] Number of outputs to read from DUT.
    );
