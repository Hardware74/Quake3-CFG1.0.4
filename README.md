# Quake3-CFG1.0.4
Quake III Arena CFG creator for the dedicated server launcher

## Overview
Quake3-CFG is a configuration management tool designed to enhance your gaming experience in Quake III Arena. This version, v1.0.4, introduces several new features aimed at providing better customization and enhanced server performance.

## New Features 1.0.4
- **CTF Specific Variables Added**: GUI change to enable "Captures to win" value, output to set variables for CTF .cfg only ensuring bots are enabled, inactivity kick after 3 minutes, forced respawn disable, friendly fire disabled

## New Features 1.0.3
- **Password Protect**: Users can now secure their servers with a password, ensuring only authorized players can join.
- **Pure Server**: This feature allows servers to enforce integrity checks on files, ensuring that only "pure" files are used.
- **Client Downloads**: Clients can now automatically download required files from the server, streamlining the player experience.
- **Packet Settings**: Enhanced control over packet management settings for improved connectivity and performance.

## Installation Instructions
1. Clone the repository using Git:
   ```bash
   git clone https://github.com/Hardware74/Quake3-CFG1.0.4.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd Quake3-CFG1.0.4
   ```
3. Follow the setup instructions in the `SETUP.md` file.

## Usage Guide
### Running the Application
To run the application, execute the following command:
```bash
./Quake3-CFG1.0.4
```
### Building Executables
For building executables, use the command:
```bash
make build
```

## Configuration Tips
- Make sure to configure your server settings in the `server.cfg` file to leverage all new features.
- Refer to the `config_example.cfg` for sample configurations.

## Requirements
- Quake III Arena (minimum version required)
- A compatible operating system (List OS requirements here)

## Version History
- **v1.0.4**: CTF Specific Variables Added
- **v1.0.3**: Added password protection, pure server functionality, client downloads, and packet settings.
- **v1.0.2**: Minor bug fixes and performance improvements.

## Resources
- [Official Quake III Arena Website](https://www.quake3arena.com)
- [Community Forums](https://www.quake3arena.com/forums)
- [Documentation and Support](https://www.quake3arena.com/support)

For further assistance, please contact the support team or open an issue in this repository.
