# FastF1 Telemetry Analysis Project

# Python virtual environment
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Default target
.PHONY: all
all: setup run

# Create virtual environment and install dependencies
.PHONY: setup
setup: $(VENV)/pyvenv.cfg
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Setup complete! Virtual environment created and dependencies installed."

$(VENV)/pyvenv.cfg:
	python3 -m venv $(VENV)

# Run the main analysis
.PHONY: run
run: setup cache plots
	$(PYTHON) main.py

# Run specific analysis functions
.PHONY: lap-comparison
lap-comparison: setup cache plots
	$(PYTHON) -c "from main import compare_fastest_laps; compare_fastest_laps()"

.PHONY: telemetry-comparison
telemetry-comparison: setup cache plots
	$(PYTHON) -c "from main import compare_telemetry; compare_telemetry()"

.PHONY: speed-analysis
speed-analysis: setup cache plots
	$(PYTHON) -c "from main import speed_analysis; speed_analysis()"

# Interactive mode with IPython
.PHONY: interactive
interactive: setup cache
	$(PIP) install ipython
	$(PYTHON) -c "import fastf1; fastf1.Cache.enable_cache('cache'); exec(open('main.py').read())"

# Clean up generated files
.PHONY: clean
clean:
	rm -rf cache/
	rm -rf plots/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Clean everything including virtual environment
.PHONY: clean-all
clean-all: clean
	rm -rf $(VENV)

# Download sample data (caches recent race data)
.PHONY: download-data
download-data: setup cache
	$(PYTHON) -c "import fastf1; fastf1.Cache.enable_cache('cache'); session = fastf1.get_session(2024, 'Las Vegas', 'R'); session.load()"

# Create cache directory
cache:
	mkdir -p cache

# Create plots directory
plots:
	mkdir -p plots

# Help target
.PHONY: help
help:
	@echo "FastF1 Telemetry Analysis Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  setup              - Create virtual environment and install dependencies"
	@echo "  run                - Run the main analysis script"
	@echo "  lap-comparison     - Compare fastest laps between drivers"
	@echo "  telemetry-comparison - Compare telemetry data between drivers"
	@echo "  speed-analysis     - Analyze speed data"
	@echo "  interactive        - Start interactive Python session with FastF1"
	@echo "  download-data      - Download and cache sample race data"
	@echo "  clean              - Clean generated files and cache"
	@echo "  clean-all          - Clean everything including virtual environment"
	@echo "  help               - Show this help message"