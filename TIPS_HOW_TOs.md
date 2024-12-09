

# Tips and How tos
## usefull cmds

For testing, create the knowledge graph. There must be some docker somewhere
```bash
poetry run python ./create_knowledge_graph.py
```
imports the data using template_package/adapters/brapi_adapter.py
This code runs:
- _preprocess_data : to open data files
- get_nodes: to create each node according to the properties in config/schema_config.yaml
- get_edges: to create each edge/relation according to the properties in config/schema_config.yaml
- 
  
Run   ./create_knowledge_graph.py, runs the neo4j docker and the biochatter docker
```bash
docker compose up
```
To really clean, do it regularly (very regularly)
```bash
docker compose down --volumes
```
