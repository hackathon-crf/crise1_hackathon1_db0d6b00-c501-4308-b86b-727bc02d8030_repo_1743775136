# ForgeAI Default Application

Welcome to the ForgeAI Default Application. This serves as an example to help you understand the structure and guidelines for automating and managing applications built on ForgeAI.

## Important Guidelines for Application Automation and Management

### Backend and Frontend Files
- **Backend Code**: Keep the main backend logic in `main_back.py`.
- **Frontend Code**: Keep the main frontend logic in `main_front.py`.
- **Start Script**: Do not modify the `start.sh` script, as it is essential for running the application correctly.


### Instructions for Updating config.toml
    If you need to update the config.toml file, please follow these guidelines:

        Avoid to use the [server] block in the config.toml file:
    
            - If your updates do not require changes to the [server] block, it is best to leave it as is.
        
        If the [server] block is necessary:
        
            - make sure to Add the [server] block at the end of the config.toml file to avoid conflicts or misconfigurations.


### Example of How to use [server] block in Config.toml file:

##### configuration blocks without [server] block
       [client]
       toolbarMode="viewer"
       showSidebarNavigation = false
       [theme]
       base = "light"

##### Add the [server] block at the end
       [client]
       toolbarMode="viewer"
       showSidebarNavigation = false
       [theme]
       base = "light"
       [server]
       runOnSave= true
       
### Directory Management
- Do not rename or delete any of the existing directories. These are important for the structure and automation of the application.
- You are free to create additional directories as needed to organize your project effectively.
- Following these guidelines ensures smooth automation, easier management, and better collaboration across teams.

## ForgeAI GenAI Services

ForgeAI offers a suite of **Generative AI (GenAI)** services, including:
- Retrieval-Augmented Generation (RAG)
- AI Chatbots
- And more...

To explore the full range of GenAI services and learn how to integrate them into your applications, please refer to the ForgeAI GenAI services repository:
[ForgeAI GenAI Services Repository](https://github.com/Forgeai-platform/forgeai-services)

This repository provides comprehensive documentation on available services, how to use them, and best practices for integration.
