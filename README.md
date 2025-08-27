# Pub/Sub to Kafka Bridge Service

A Python service that acts as a bridge between Google Cloud Pub/Sub and Apache Kafka, specifically designed to relay GCS (Google Cloud Storage) upload events for PDF files from Pub/Sub subscriptions to Kafka topics.

## Overview

This service subscribes to Google Cloud Pub/Sub messages triggered by GCS file uploads, filters for PDF files, transforms the message format, and forwards them to Kafka topics for downstream processing. It includes heartbeat logging and error handling for reliable message processing.

## Features

- **Pub/Sub Integration**: Subscribes to GCS upload notifications via Pub/Sub
- **PDF Filtering**: Only processes messages for PDF file uploads
- **Message Transformation**: Converts Pub/Sub messages to Kafka-compatible format
- **Kafka Producer**: Forwards processed messages to specified Kafka topics
- **Error Handling**: Comprehensive logging and error recovery mechanisms
- **Heartbeat Monitoring**: Regular status logging for service health monitoring
- **Containerized**: Includes Dockerfile and Jenkins pipeline for deployment

## Message Flow

1. GCS file upload triggers Pub/Sub notification
2. Service receives and validates message (PDF files only)
3. Message transformed to include bucket, file path, and metadata
4. Forwarded to Kafka topic for consumption by downstream services

## Message Format

**Input (Pub/Sub):** GCS notification with file metadata  
**Output (Kafka):** Structured JSON with bucket, file path, event type, and source information for downstream PDF processing services.
