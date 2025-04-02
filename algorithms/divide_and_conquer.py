def divide_regions(nodes, k=2):
    return [nodes[:len(nodes)//k], nodes[len(nodes)//k:]]

def merge_solutions(regional_solutions):
    merged_routes = {}
    merged_packages = []
    for solution in regional_solutions:
        merged_routes.update(solution['route'])
        merged_packages.extend(solution['packages'])
    return {'route': merged_routes, 'packages': merged_packages}