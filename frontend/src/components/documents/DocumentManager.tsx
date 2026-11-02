import React, { useState } from 'react';
import { 
  FileText, 
  Search, 
  Trash2, 
  Upload, 
  RefreshCw, 
  Layers, 
  CheckCircle, 
  HardDrive,
  AlertCircle
} from 'lucide-react';
import { DocumentItem } from '../../types';
import { deleteDocument } from '../../services/api';

interface DocumentManagerProps {
  documents: DocumentItem[];
  totalChunks: number;
  onRefresh: () => void;
  onOpenUpload: () => void;
}

export const DocumentManager: React.FC<DocumentManagerProps> = ({
  documents,
  totalChunks,
  onRefresh,
  onOpenUpload,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  const filteredDocs = documents.filter((doc) =>
    doc.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleDelete = async (filename: string) => {
    if (!window.confirm(`Are you sure you want to delete ${filename} and remove its embeddings from ChromaDB?`)) {
      return;
    }
    setDeletingId(filename);
    setActionError(null);
    try {
      await deleteDocument(filename);
      onRefresh();
    } catch (err: any) {
      setActionError(err.message || 'Failed to delete document.');
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-8 max-w-6xl mx-auto w-full">
      {/* Top Banner Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white">{documents.length}</div>
              <div className="text-xs text-slate-400">Total Indexed Documents</div>
            </div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white">{totalChunks}</div>
              <div className="text-xs text-slate-400">Embedded Chunks in ChromaDB</div>
            </div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <HardDrive className="w-5 h-5" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white">
                {documents.reduce((acc, d) => acc + d.size_mb, 0).toFixed(2)} MB
              </div>
              <div className="text-xs text-slate-400">Total Storage Footprint</div>
            </div>
          </div>
        </div>
      </div>

      {actionError && (
        <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center gap-2.5 text-xs text-rose-300">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
          <span>{actionError}</span>
        </div>
      )}

      {/* Action Toolbar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search documents by name..."
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500/50"
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
          <button
            onClick={onRefresh}
            className="p-2 rounded-xl bg-slate-900/80 hover:bg-slate-800 border border-slate-800 text-slate-400 hover:text-white transition-colors"
            title="Refresh documents list"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <button
            onClick={onOpenUpload}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold shadow-md shadow-blue-500/20 transition-all"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Upload Document</span>
          </button>
        </div>
      </div>

      {/* Documents Table / Card List */}
      <div className="rounded-2xl bg-slate-900/60 border border-slate-800/80 overflow-hidden backdrop-blur-md">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950/60 border-b border-slate-800 text-slate-400 font-bold uppercase tracking-wider text-[10px]">
            <tr>
              <th className="py-3.5 px-5">Document Name</th>
              <th className="py-3.5 px-4">Size</th>
              <th className="py-3.5 px-4">Chunks</th>
              <th className="py-3.5 px-4">Last Modified</th>
              <th className="py-3.5 px-4">Status</th>
              <th className="py-3.5 px-5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {filteredDocs.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-12 text-center text-slate-500">
                  {searchQuery ? 'No documents match your search query.' : 'No documents in repository. Upload a PDF to begin.'}
                </td>
              </tr>
            ) : (
              filteredDocs.map((doc) => (
                <tr key={doc.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-4 px-5 font-medium text-white flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center shrink-0">
                      <FileText className="w-4 h-4 text-blue-400" />
                    </div>
                    <span className="truncate max-w-xs">{doc.name}</span>
                  </td>
                  <td className="py-4 px-4 text-slate-400">{doc.size_mb} MB</td>
                  <td className="py-4 px-4 font-mono text-slate-300">
                    <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">
                      {doc.chunks_count} chunks
                    </span>
                  </td>
                  <td className="py-4 px-4 text-slate-400">{doc.updated_at}</td>
                  <td className="py-4 px-4">
                    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-semibold text-[11px]">
                      <CheckCircle className="w-3 h-3" />
                      {doc.status}
                    </span>
                  </td>
                  <td className="py-4 px-5 text-right">
                    <button
                      onClick={() => handleDelete(doc.name)}
                      disabled={deletingId === doc.name}
                      className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors disabled:opacity-50"
                      title="Delete document and ChromaDB vectors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
