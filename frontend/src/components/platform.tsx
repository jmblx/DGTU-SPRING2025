import React from "react";

type Player = {
    id: string;
    x: number;
    y: number;
};

interface PlatformProps {
    players: Player[];
}

const Platform: React.FC<PlatformProps> = ({ players }) => {
    return (
        <div className="relative w-[800px] h-[400px] bg-gray-200 border rounded">
            {players.map((player) => (
                <div
                    key={player.id}
                    className="absolute w-6 h-6 bg-blue-500 rounded-full transition-all duration-100"
                    style={{
                        left: `${player.x}px`,
                        top: `${player.y}px`,
                    }}
                />
            ))}
        </div>
    );
};

export default Platform;
