import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
  Avatar,
  Tooltip,
  IconButton
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Speed,
  Refresh
} from '@mui/icons-material';

const CryptoCard = ({ symbol, data, formatCurrency, formatPercentage }) => {
  const {
    price_usd,
    market_cap,
    volume_24h,
    price_change_24h,
    timestamp,
    last_updated
  } = data;

  const formatMarketCap = (value) => {
    if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`;
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
    if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
    return formatCurrency(value);
  };

  const formatVolume = (value) => {
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
    if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
    return formatCurrency(value);
  };

  const getCryptoAvatar = (symbol) => {
    const colors = {
      'BITCOIN': '#F7931A',
      'ETHEREUM': '#627EEA',
      'BINANCECOIN': '#F3BA2F',
      'SOLANA': '#14F195',
      'CARDANO': '#0033AD',
      'CHAINLINK': '#2A5ADA',
      'POLKADOT': '#E6007A',
      'LITECOIN': '#BFBBBB'
    };
    return colors[symbol] || '#2196F3';
  };

  const getChangeIntensity = (change) => {
    const absChange = Math.abs(change);
    if (absChange > 10) return 'High';
    if (absChange > 5) return 'Medium';
    return 'Low';
  };

  const getVolatilityColor = (volatility) => {
    switch (volatility) {
      case 'High': return '#F44336';
      case 'Medium': return '#FF9800';
      case 'Low': return '#4CAF50';
      default: return '#4CAF50';
    }
  };

  return (
    <Card sx={{
      background: 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: 3,
      transition: 'all 0.3s ease',
      height: '100%',
      '&:hover': {
        transform: 'translateY(-4px)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
        borderColor: 'rgba(255,255,255,0.2)'
      }
    }}>
      <CardContent sx={{ p: 3 }}>
        {/* Header Section - Fixed Alignment */}
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Box display="flex" alignItems="center" flex={1}>
            <Avatar
              sx={{
                bgcolor: getCryptoAvatar(symbol),
                width: 40,
                height: 40,
                mr: 2,
                fontSize: '1rem',
                fontWeight: 'bold',
                border: '2px solid rgba(255,255,255,0.1)'
              }}
            >
              {symbol.charAt(0)}
            </Avatar>
            <Box>
              <Typography variant="h6" fontWeight="bold" sx={{ color: 'white', lineHeight: 1.2 }}>
                {symbol}
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.8rem' }}>
                {symbol === 'BINANCECOIN' ? 'Binance Coin' : 
                 symbol === 'CHAINLINK' ? 'Chainlink' :
                 symbol.charAt(0) + symbol.slice(1).toLowerCase()}
              </Typography>
            </Box>
          </Box>
          <Chip
            label="Live"
            size="small"
            sx={{
              bgcolor: '#4CAF50',
              color: 'white',
              fontWeight: 'bold',
              fontSize: '0.7rem',
              height: 24
            }}
          />
        </Box>

        {/* Price and Change Section - All on One Line */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="h4" fontWeight="bold" sx={{ color: 'white', lineHeight: 1.2 }}>
              {formatCurrency(price_usd)}
            </Typography>
            <Box display="flex" alignItems="center" gap={0.5}>
              {price_change_24h >= 0 ? (
                <TrendingUp sx={{ color: '#4CAF50', fontSize: 16 }} />
              ) : (
                <TrendingDown sx={{ color: '#F44336', fontSize: 16 }} />
              )}
              <Typography
                variant="body1"
                fontWeight="bold"
                sx={{
                  color: price_change_24h >= 0 ? '#4CAF50' : '#F44336',
                  fontSize: '0.9rem'
                }}
              >
                {formatPercentage(price_change_24h)}
              </Typography>
            </Box>
          </Box>
          <Chip
            label={`${getChangeIntensity(price_change_24h)} Volatility`}
            size="small"
            sx={{
              bgcolor: getVolatilityColor(getChangeIntensity(price_change_24h)),
              color: 'white',
              fontWeight: 'bold',
              fontSize: '0.7rem',
              height: 24,
              minWidth: 80
            }}
          />
        </Box>

        {/* Market Data Section - Better Alignment */}
        <Box sx={{ mb: 2 }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.8rem' }}>
              $ Market Cap
            </Typography>
            <Typography variant="body2" fontWeight="bold" sx={{ color: 'white', fontSize: '0.8rem' }}>
              {formatMarketCap(market_cap)}
            </Typography>
          </Box>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.8rem' }}>
              24h Volume
            </Typography>
            <Typography variant="body2" fontWeight="bold" sx={{ color: 'white', fontSize: '0.8rem' }}>
              {formatVolume(volume_24h)}
            </Typography>
          </Box>
        </Box>

        {/* Price Trend Section - Improved Alignment */}
        <Box sx={{ mb: 2 }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.8rem' }}>
              Price Trend
            </Typography>
            <Typography
              variant="body2"
              fontWeight="bold"
              sx={{
                color: price_change_24h >= 0 ? '#4CAF50' : '#F44336',
                fontSize: '0.8rem'
              }}
            >
              {price_change_24h >= 0 ? 'Bullish' : 'Bearish'}
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={Math.min(Math.abs(price_change_24h) * 10, 100)}
            sx={{
              height: 6,
              borderRadius: 3,
              bgcolor: 'rgba(255,255,255,0.1)',
              '& .MuiLinearProgress-bar': {
                bgcolor: price_change_24h >= 0 ? '#4CAF50' : '#F44336',
                borderRadius: 3
              }
            }}
          />
        </Box>

        {/* Footer Section - Better Alignment */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.7rem' }}>
              Updated: {new Date(timestamp || last_updated).toLocaleTimeString()}
            </Typography>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.7rem', display: 'block', mt: 0.5 }}>
              Powered by AWS Kinesis
            </Typography>
          </Box>
          <Tooltip title="Refresh Data">
            <IconButton size="small" sx={{ color: 'rgba(255,255,255,0.5)' }}>
              <Refresh sx={{ fontSize: 16 }} />
            </IconButton>
          </Tooltip>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CryptoCard; 