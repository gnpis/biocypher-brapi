from biocypher import BioCypher, Resource
from template_package.adapters.brapi_adapter import BrapiAdapter

adapter = BrapiAdapter()
bc = BioCypher()
# Create a knowledge graph from the adapter
bc.write_nodes(adapter.get_nodes())
bc.write_edges(adapter.get_edges())

# Write admin import statement
bc.write_import_call()

# Print summary
bc.summary()
