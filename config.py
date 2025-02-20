class ConfigHandler:
    def __init__(self):
        self.config_file = "config"
        self.config = {}
        self.read()

    def read(self):
        """Reads the configuration file into a dictionary."""
        try:
            with open(self.config_file, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):  # Skip empty lines or comments
                        continue
                    key, value = line.split("=", 1)
                    self.config[key.strip()] = int(value.strip()) or value.strip()
        except OSError:
            print(f"Config file '{self.config_file}' not found.")

    def write(self):
        """Writes the configuration dictionary to a file."""
        with open(self.config_file, "w") as file:
            for key, value in self.config.items():
                file.write(f"{key}={value}\n")

    def update(self, key, value):
        """Updates a configuration key with a new value."""
        self.config[key] = value
