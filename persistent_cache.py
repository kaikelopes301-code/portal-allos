# persistent_cache.py — Cache persistente em disco (opcional)

import pickle
import json
from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import hashlib


class PersistentCache:
    """Cache persistente em disco com expiração."""
    
    def __init__(self, cache_dir: Path, ttl_hours: int = 24):
        """
        Args:
            cache_dir: Diretório para armazenar cache
            ttl_hours: Tempo de vida do cache em horas
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.metadata_file = self.cache_dir / "_metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Carrega metadados do cache."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except Exception:
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Salva metadados do cache."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            print(f"Aviso: Não foi possível salvar metadata: {e}")
    
    def _make_key(self, key: str) -> str:
        """Gera hash seguro para usar como nome de arquivo."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Recupera valor do cache.
        
        Args:
            key: Chave do cache
            default: Valor padrão se não encontrar
        
        Returns:
            Valor armazenado ou default
        """
        file_key = self._make_key(key)
        cache_file = self.cache_dir / f"{file_key}.pkl"
        
        # Verifica se existe
        if not cache_file.exists():
            return default
        
        # Verifica expiração
        if key in self.metadata:
            created = datetime.fromisoformat(self.metadata[key]['created'])
            if datetime.now() - created > self.ttl:
                # Expirado - remove
                self.delete(key)
                return default
        
        # Carrega valor
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Aviso: Erro ao carregar cache '{key}': {e}")
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """Armazena valor no cache.
        
        Args:
            key: Chave do cache
            value: Valor a armazenar
        
        Returns:
            True se sucesso
        """
        file_key = self._make_key(key)
        cache_file = self.cache_dir / f"{file_key}.pkl"
        
        try:
            # Salva valor
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
            
            # Atualiza metadata
            self.metadata[key] = {
                'created': datetime.now().isoformat(),
                'file': str(cache_file.name),
                'size_bytes': cache_file.stat().st_size
            }
            self._save_metadata()
            
            return True
        except Exception as e:
            print(f"Erro ao salvar cache '{key}': {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Remove valor do cache."""
        file_key = self._make_key(key)
        cache_file = self.cache_dir / f"{file_key}.pkl"
        
        try:
            if cache_file.exists():
                cache_file.unlink()
            if key in self.metadata:
                del self.metadata[key]
                self._save_metadata()
            return True
        except Exception as e:
            print(f"Erro ao deletar cache '{key}': {e}")
            return False
    
    def clear(self) -> int:
        """Limpa todo o cache."""
        count = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            try:
                cache_file.unlink()
                count += 1
            except Exception:
                pass
        
        self.metadata.clear()
        self._save_metadata()
        return count
    
    def cleanup_expired(self) -> int:
        """Remove apenas itens expirados."""
        count = 0
        now = datetime.now()
        expired_keys = []
        
        for key, meta in self.metadata.items():
            created = datetime.fromisoformat(meta['created'])
            if now - created > self.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            if self.delete(key):
                count += 1
        
        return count
    
    def stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        total_size = sum(
            (self.cache_dir / meta['file']).stat().st_size 
            for meta in self.metadata.values()
            if (self.cache_dir / meta['file']).exists()
        )
        
        return {
            'items': len(self.metadata),
            'total_size_mb': total_size / 1024 / 1024,
            'cache_dir': str(self.cache_dir),
            'ttl_hours': self.ttl.total_seconds() / 3600,
            'oldest_item': min(
                (datetime.fromisoformat(m['created']) for m in self.metadata.values()),
                default=None
            ).isoformat() if self.metadata else None
        }


# Exemplo de uso com Excel sheets
class CachedExtractor:
    """Extractor com cache persistente em disco."""
    
    def __init__(self, xlsx_dir: Path, cache_dir: Optional[Path] = None):
        from extractor_optimized import Extractor
        
        self.extractor = Extractor(xlsx_dir)
        
        if cache_dir is None:
            cache_dir = xlsx_dir / ".cache"
        
        self.cache = PersistentCache(cache_dir, ttl_hours=24)
    
    def read_region_sheet(self, path: Path, regiao: str):
        """Lê sheet com cache persistente."""
        # Chave do cache: caminho + região + mtime do arquivo
        mtime = path.stat().st_mtime
        cache_key = f"{path}:{regiao}:{mtime}"
        
        # Tenta recuperar do cache
        cached = self.cache.get(cache_key)
        if cached is not None:
            print(f"✓ Cache hit: {path.name} - {regiao}")
            return cached
        
        # Cache miss - lê do Excel
        print(f"↻ Cache miss: {path.name} - {regiao} (lendo...)")
        result = self.extractor.read_region_sheet(path, regiao, use_cache=False)
        
        # Armazena no cache
        self.cache.set(cache_key, result)
        
        return result
    
    def cleanup_cache(self):
        """Limpa cache expirado."""
        removed = self.cache.cleanup_expired()
        print(f"✓ {removed} item(ns) expirado(s) removido(s)")
    
    def clear_cache(self):
        """Limpa todo o cache."""
        count = self.cache.clear()
        print(f"✓ {count} item(ns) removido(s) do cache")


# Uso no main.py:
# extractor = CachedExtractor(Path(args.xlsx_dir))
# df, sheet = extractor.read_region_sheet(workbook, args.regiao)