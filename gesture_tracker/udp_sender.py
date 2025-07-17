import socket
import json
import gzip
import struct

class UDPSender:
    def __init__(self, ip="127.0.0.1", port=7777):
        self.ip = ip
        self.port = port
        self.buffer_size = 65507  # Taille max UDP (65535 - 28 bytes header)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"📡 UDP Sender initialisé: {ip}:{port}")
    
    def send_packet(self, packet, universe=0, compress=True):
        """Envoie le packet via UDP avec protocole eHuB"""
        try:
            # Convertir le packet en JSON puis en bytes
            json_data = json.dumps(packet).encode('utf-8')
            
            # Compression
            if compress:
                payload = gzip.compress(json_data)
                msg_type = 2  # Type 2 = compressé
                original_size = len(json_data)
                compressed_size = len(payload)
                compression_ratio = (1 - compressed_size / original_size) * 100
                print(f"📦 Compression: {original_size} → {compressed_size} bytes ({compression_ratio:.1f}% réduction)")
            else:
                payload = json_data
                msg_type = 1  # Type 1 = non compressé
            
            # Construire le header eHuB
            entity_count = len(packet)
            payload_size = len(payload)
            
            # Format: "eHuB" + msgType(1) + universe(1) + entityCount(2) + payloadSize(2) + payload
            header = struct.pack(
                '<4sBBHH',  # little-endian: 4 chars + byte + byte + uint16 + uint16
                b'eHuB',    # Magic header
                msg_type,   # Type de message (1=raw, 2=compressed)
                universe,   # Univers (0 par défaut)
                entity_count,  # Nombre d'entités
                payload_size   # Taille du payload
            )
            
            # Assembler le message final
            full_message = header + payload
            
            # Vérifier la taille totale
            if len(full_message) > self.buffer_size:
                print(f"⚠️ Message trop gros ({len(full_message)} bytes)")
                return False
            
            # Envoyer
            self.sock.sendto(full_message, (self.ip, self.port))
            print(f"📡 Packet eHuB envoyé: {len(full_message)} bytes (header: 10, payload: {payload_size})")
            print(f"   → Type: {msg_type}, Universe: {universe}, Entities: {entity_count}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur UDP: {e}")
            return False
    
    def close(self):
        """Ferme la connexion UDP"""
        self.sock.close()
        print("🔌 Connexion UDP fermée")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()