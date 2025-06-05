# ===== PROJEK STRUKDAT: Rute Tercepat & TSP (Brute-force) di Inggris =====

import itertools
import networkx as nx
import matplotlib.pyplot as plt

# ====== Kelas Graph dengan adjacency list ======
class Graph:
    # Membuat adjacency list untuk setiap kota
    def __init__(self, cities): 
        self.cities = cities
        self.adj = {city: [] for city in cities}

    # Menambahkan edge dua arah antara kota u dan v dengan bobot w
    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))
    
    # Algoritma Dijkstra untuk mencari rute tercepat dari kota asal ke kota tujuan
    def dijkstra(self, asal, tujuan):
        import heapq
        heap = [(0, asal, [asal])]
        visited = set()
        while heap:
            cost, u, path = heapq.heappop(heap)
            if u == tujuan:
                return path, cost
            if u in visited:
                continue
            visited.add(u)
            for v, w in self.adj[u]:
                if v not in visited:
                    heapq.heappush(heap, (cost + w, v, path + [v]))
        return None, float('inf')
    
    # Brute-force TSP: mencari rute terpendek melewati semua kota (tanpa kembali ke asal)
    def tsp_bruteforce(self, asal):
        import functools
        kota_lain = [k for k in self.cities if k != asal]
        min_path = None
        min_cost = float('inf')
        # Memoization untuk Dijkstra antar kota
        dijkstra_cache = {}
        # Mengambil cost Dijkstra dari u ke v, simpan jika sudah pernah dihitung
        def get_cost(u, v):
            key = tuple(sorted([u, v]))
            if key not in dijkstra_cache:
                _, w = self.dijkstra(u, v)
                dijkstra_cache[key] = w
            return dijkstra_cache[key]
         # Cek semua permutasi kota lain
        for perm in itertools.permutations(kota_lain):
            path = [asal] + list(perm)
            total = 0
            feasible = True
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                w = get_cost(u, v)
                if w == float('inf'):
                    feasible = False
                    break
                total += w
                # Cek apakah total cost melebihi minimum yang sudah ditemukan
                if total >= min_cost:
                    feasible = False
                    break
            if feasible and total < min_cost:
                min_cost = total
                min_path = path
        return min_path, min_cost

# ====== Data kota dan edge ======
cities = [
    "London", "Birmingham", "Manchester", "Liverpool", "Edinburgh",
    "Glasgow", "Leeds", "Bristol", "Newcastle", "Sheffield"
]
edges = [
    ("London", "Birmingham", 205), ("London", "Manchester", 335), ("London", "Liverpool", 335),
    ("London", "Edinburgh", 665), ("London", "Glasgow", 640), ("London", "Leeds", 310),
    ("London", "Bristol", 190), ("London", "Newcastle", 450), ("London", "Sheffield", 270),
    ("Birmingham", "Manchester", 140), ("Birmingham", "Liverpool", 160), ("Birmingham", "Edinburgh", 470),
    ("Birmingham", "Glasgow", 450), ("Birmingham", "Leeds", 170), ("Birmingham", "Bristol", 140),
    ("Birmingham", "Newcastle", 330), ("Birmingham", "Sheffield", 130), ("Manchester", "Liverpool", 55),
    ("Manchester", "Edinburgh", 355), ("Manchester", "Glasgow",350), ("Manchester", "Leeds",70),
    ("Manchester", "Bristol", 270), ("Manchester", "Newcastle", 230), ("Manchester", "Sheffield", 65),
    ("Liverpool", "Edinburgh", 355), ("Liverpool", "Glasgow", 350), ("Liverpool", "Leeds", 120),
    ("Liverpool", "Newcastle", 280), ("Liverpool", "Sheffield", 110), ("Edinburgh", "Glasgow", 75)
]
# ====== Membuat graph untuk 3 mode transportasi dengan bobot waktu tempuh (jam) ======
kecepatan = {
    "Jalan Kaki": 5,
    "Sepeda": 20,
    "Mobil": 60
}

graphs = {}
for mode, speed in kecepatan.items():
    # Membuat graph untuk setiap mode transportasi
    G = Graph(cities)
    for u, v, jarak in edges:
        waktu = round(jarak / speed, 2)
        G.add_edge(u, v, waktu)
    graphs[mode] = G
# Graph untuk jarak (km) saja
graph = Graph(cities)
for u, v, w in edges:
    graph.add_edge(u, v, w)
    
# Membuat graph NetworkX untuk visualisasi dengan bobot waktu tempuh
def make_graph(edges, speed_factor):
    G = nx.Graph()
    for u, v, km in edges:
        waktu = round((km / speed_factor), 2)
        G.add_edge(u, v, weight=waktu, km=km)
    return G
# Membuat graph NetworkX untuk visualisasi tiap mode
speed_walk, speed_bike, speed_car = 5, 20, 60
G_walk = make_graph(edges, speed_walk)
G_bike = make_graph(edges, speed_bike)
G_car = make_graph(edges, speed_car)

# ====== Visualisasi graph ======
G_km = nx.Graph()
for u, v, km in edges:
    G_km.add_edge(u, v, weight=km)
    
# Posisi node untuk visualisasi             
pos = {
    "London": (0, 2), "Birmingham": (2, 3), "Manchester": (4, 3), "Liverpool": (6, 2),
    "Edinburgh": (8, 4), "Glasgow": (8, 6), "Leeds": (4, 5), "Bristol": (1, 0),
    "Newcastle": (7, 5), "Sheffield": (5, 1)
}

# Visualisasi peta kota & jarak antar kota (km)
def visualisasi_graph_awal():
    plt.figure(figsize=(13,8))
    nx.draw_networkx_nodes(G_km, pos, node_color='orange', node_size=1700, edgecolors='orange')
    nx.draw_networkx_edges(G_km, pos, width=2, edge_color='green')
    nx.draw_networkx_labels(G_km, pos, font_size=13, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G_km, 'weight')
    edge_labels_km = {k: f"{v} km" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G_km, pos, edge_labels=edge_labels_km, font_color='red', font_size=11, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))
    plt.title("Peta Kota & Jarak Antar Kota (km)", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    
 # Fungsi untuk menghitung total jarak dari rute yang diberikan
def total_jarak(path):
    total = 0
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        for a, b, km in edges:
            if (a == u and b == v) or (a == v and b == u):
                total += km
                break
    return total

# ====== Menu utama dan proses utama ======
def main():
    # Menampilkan judul & informasi kelompok
    print("===== PROJEK STRUKDAT: Program Peta dan GPS Sederhana =====")
    print("KELOMPOK 5 STRUKDAT")
    print("Anggota:")
    print("1. 24091397108 - Janatul Fitri")
    print("2. 24091397125 - Anatoly Aquila Katimin")
    print("3. 24091397128 - Alida Nayla Faizah")
    print("=====================================")
    
    # Visualisasi graph awal (peta dan waktu tempuh)
    visualisasi_graph_awal()
    while True:
        print("\nPilihan menu:")
        print("1. Rute tercepat Dijkstra")
        print("2. Rute TSP Brute-force (tanpa kembali ke asal)")
        print("3. Keluar")
        pil = input("Pilih menu (1-3): ").strip()
        if pil == "1":
            # ====== Menu Algoritma Dijkstra ======
            print("\nDaftar Kota:", ', '.join(cities))
            asal = input("Masukkan kota asal: ").strip()
            while asal not in cities:
                print("Nama kota tidak valid! Pilih sesuai daftar di atas.")
                asal = input("Masukkan kota asal: ").strip()
            tujuan = input("Masukkan kota tujuan: ").strip()
            while tujuan not in cities:
                print("Nama kota tidak valid! Pilih sesuai daftar di atas.")
                tujuan = input("Masukkan kota tujuan: ").strip()
            print("Pilih mode transportasi:")
            print("1. Jalan Kaki\n2. Sepeda\n3. Mobil")
            pilih_mod = input("Pilihan (1/2/3): ").strip()
            mode = "Jalan Kaki" if pilih_mod == "1" else "Sepeda" if pilih_mod == "2" else "Mobil"
            G_graph = graphs[mode]  # Untuk perhitungan Dijkstra pada (class Graph)
            path, waktu = G_graph.dijkstra(asal, tujuan)
            if path:
                jarak = total_jarak(path)
                print(f"\nTransportasi: {mode}")
                print(f"Jalur tercepat antar kota: {' -> '.join(path)}")
                print(f"Total waktu tempuh: {waktu} jam")
                print(f"Total jarak tempuh: {jarak} km")
                    
                # Visualisasi hasil Dijkstra: rute tercepat & jarak antar kota
                plt.figure(figsize=(12,8))
                nx.draw_networkx_nodes(G_km, pos, node_color='orange', node_size=2000, edgecolors='orange')
                nx.draw_networkx_edges(G_km, pos, width=2, edge_color='green')
                nx.draw_networkx_labels(G_km, pos, font_size=13, font_weight='bold')
                path_edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G_km, pos, edgelist=path_edges, width=4, edge_color='red')
                # Label jarak antar kota pada rute tercepat
                edge_labels = {}
                for u, v in path_edges:
                    for a, b, km in edges:
                        if (a == u and b == v) or (a == v and b == u):
                            edge_labels[(u, v)] = f"{km} km"
                            break
                nx.draw_networkx_edge_labels(G_km, pos, edge_labels=edge_labels, font_color='red', font_size=12, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))
                plt.title(f"Rute tercepat {asal} ke {tujuan} menggunakan ({mode})", fontsize=16)
                plt.axis('off')
                plt.tight_layout()
                plt.show()
            else:
                print("Tidak ada jalur.")
        elif pil == "2":
            # ======= Menu Algoritma Traveling Salesman Problem (brute-force) ========
            print("\nDaftar Kota:", ', '.join(cities))
            asal_tsp = input("Kota awal TSP: ").strip()
            while asal_tsp not in cities:
                print("Nama kota tidak valid! Pilih sesuai daftar di atas.")
                asal_tsp = input("Kota awal TSP: ").strip()
            print("Pilih mode transportasi:")
            print("1. Jalan Kaki\n2. Sepeda\n3. Mobil")
            pilih_mod = input("Pilihan (1/2/3): ").strip()
            mode = "Jalan Kaki" if pilih_mod == "1" else "Sepeda" if pilih_mod == "2" else "Mobil"
            G = graphs[mode]
            print(f"\nProses TSP {mode} ...")
            print("Program sedang menghitung TSP, mohon tunggu sebentar...")
            path, total_cost = G.tsp_bruteforce(asal_tsp)
            if path:
                jarak = total_jarak(path)
                print(f"Rute TSP terbaik: {' -> '.join(path)}")
                print(f"Total waktu tempuh: {total_cost} jam")
                print(f"Total jarak tempuh: {jarak} km")
                
                # Visualisasi hasil TSP: tampilkan rute TSP & jarak antar kota
                plt.figure(figsize=(12,8))
                nx.draw_networkx_nodes(G_km, pos, node_color='orange', node_size=2000, edgecolors='orange')
                nx.draw_networkx_edges(G_km, pos, width=2, edge_color='green')
                nx.draw_networkx_labels(G_km, pos, font_size=13, font_weight='bold')
                # Highlight rute TSP
                path_edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G_km, pos, edgelist=path_edges, width=4, edge_color='blue')
                # Label jarak antar kota pada rute TSP
                edge_labels = {}
                for u, v in path_edges:
                    for a, b, km in edges:
                        if (a == u and b == v) or (a == v and b == u):
                            edge_labels[(u, v)] = f"{km} km"
                            break
                nx.draw_networkx_edge_labels(G_km, pos, edge_labels=edge_labels, font_color='blue', font_size=12, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))
                plt.title(f"Rute TSP {asal_tsp} menggunakan ({mode})", fontsize=16)
                plt.axis('off')
                plt.tight_layout()
                plt.show()
            else:
                print("Tidak ada jalur.")
        elif pil == "3":
            # Keluar dari program
            print("=== Program selesai ===")
            print("===== Terima kasih sudah menggunakan Maps dan GPS Sederhana!! =====")
            break
        else:
            print("Pilihan tidak valid!")
            
if __name__ == "__main__":
    main()
