import React, { useRef, useEffect } from 'react';
import { EmptyState } from './EmptyState';
import { MessageBubble } from './MessageBubble';
import { ChatComposer } from './ChatComposer';
import { Message } from '../../types';

interface ChatWorkspaceProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  onOpenUpload: () => void;
  isProcessing: boolean;
}

export const ChatWorkspace: React.FC<ChatWorkspaceProps> = ({
  messages,
  onSendMessage,
  onOpenUpload,
  isProcessing,
}) => {
  const scrollEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isProcessing]);

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden relative">
      {/* Scrollable Conversation Stream */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
        {messages.length === 0 ? (
          <EmptyState onSelectSuggestion={onSendMessage} />
        ) : (
          <div className="max-w-4xl mx-auto">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            <div ref={scrollEndRef} />
          </div>
        )}
      </div>

      {/* Docked Bottom Chat Input */}
      <ChatComposer
        onSendMessage={onSendMessage}
        onOpenUpload={onOpenUpload}
        isProcessing={isProcessing}
      />
    </div>
  );
};
