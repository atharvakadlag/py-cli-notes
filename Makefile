# Define variables
SCRIPT_NAME=app.py
TARGET_NAME=notes
INSTALL_DIR=/usr/local/bin

# Default target
all: install

# Make the script executable and move it to the install directory
install:
	chmod +x $(SCRIPT_NAME)
	sudo cp $(SCRIPT_NAME) $(INSTALL_DIR)/$(TARGET_NAME)

# Clean target (optional)
clean:
	# Add any cleanup commands here if needed
	@echo "Nothing to clean."

.PHONY: all install clean