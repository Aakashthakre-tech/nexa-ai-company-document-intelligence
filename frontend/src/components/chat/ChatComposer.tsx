import React, { useState, useRef } from 'react';
import { Send, Paperclip, Loader2, Sparkles } from 'lucide-react';

interface ChatComposerProps {
  onSendMessage: (message: string) => void;
  onOpenUpload: () => void;
  isProcessing: boolean;
}

export const ChatComposer: React.FC<ChatComposerProps> = ({
  onSendMessage,
  onOpenUpload,
  isProcessing,
}) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="p-4 border-t border-slate-800/80 bg-[#070c16]/90 backdrop-blur-xl">
      <div className="max-w-4xl mx-auto">
        {/* Processing State Indicator */}
        {isProcessing && (
          <div className="flex items-center gap-2 mb-2 text-xs text-blue-400 font-medium animate-pulse px-1">
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
            <span>Agent is querying ChromaDB & reasoning with Gemini 2.5 Flash...</span>
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="relative flex items-end gap-2 p-2 rounded-2xl bg-slate-900/90 border border-slate-800 focus-within:border-blue-500/50 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all shadow-xl shadow-black/30"
        >
          {/* File Attachment Button */}
          <button
            type="button"
            onClick={onOpenUpload}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800/80 transition-colors shrink-0 mb-0.5"
            title="Upload PDF document to knowledge base"
          >
            <Paperclip className="w-5 h-5" />
          </button>

          {/* Chat Text Input */}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isProcessing}
            placeholder="Ask Nexa anything about your knowledge base..."
            rows={1}
            className="flex-1 bg-transparent border-none outline-none resize-none text-sm text-slate-100 placeholder-slate-500 py-2 px-1 max-h-32 min-h-[40px]"
          />

          {/* Send Action Button */}
          <button
            type="submit"
            disabled={!input.trim() || isProcessing}
            className="p-2.5 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 disabled:opacity-40 disabled:hover:from-blue-600 disabled:hover:to-indigo-600 text-white shadow-md shadow-blue-500/20 transition-all shrink-0 hover:scale-105 active:scale-95 mb-0.5"
            title="Send message"
          >
            {isProcessing ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </form>

        <div className="flex items-center justify-between text-[11px] text-slate-500 px-2 mt-2">
          <span>Grounded in indexed company documents · Hallucination protected</span>
          <span>Press Enter to send, Shift+Enter for new line</span>
        </div>
      </div>
    </div>
  );
};
