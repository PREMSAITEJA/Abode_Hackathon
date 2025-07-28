FROM --platform=linux/amd64 python:3.10-slim-bullseye

# Ensure all system packages are updated to the latest versions
RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && apt-get install --no-install-recommends -y \
	ca-certificates \
	build-essential \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /sample_dataset

# Update system packages and fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
	ca-certificates \
	build-essential \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir PyMuPDF scikit-learn sentence-transformers numpy jsonschema

# Copy the processing script and schema
COPY process_pdfs.py .
COPY sample_dataset/schema ./sample_dataset/schema

# Create input and output directories
RUN mkdir -p /sample_dataset/pdfs /sample_dataset/outputs

CMD ["python", "process_pdfs.py"]