import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Divider
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  AttachMoney,
  ShowChart,
  Speed,
  Analytics,
  ArrowUpward,
  ArrowDownward,
  Star,
  TrendingFlat
} from '@mui/icons-material';

const MarketOverview = ({ analytics, formatCurrency }) => {
  const {
    total_market_cap = 0,
    total_volume_24h = 0,
    crypto_count = 0
  } = analytics || {};

  const formatCompactCurrency = (value) => {
    if (value === null || value === undefined || isNaN(value)) {
      return '$0.00';
    }
    const numValue = Number(value);
    if (numValue >= 1e12) return `$${(numValue / 1e12).toFixed(2)}T`;
    if (numValue >= 1e9) return `$${(numValue / 1e9).toFixed(2)}B`;
    if (numValue >= 1e6) return `$${(numValue / 1e6).toFixed(2)}M`;
    return formatCurrency(numValue);
  };

  return (
    <Box>
      {/* Market Statistics - Clean 3-card layout */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
            color: 'white',
            height: '100%',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: '0 8px 25px rgba(76, 175, 80, 0.3)'
            }
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <AttachMoney sx={{ mr: 1, fontSize: 28 }} />
                <Typography variant="h6">Total Market Cap</Typography>
              </Box>
              <Typography variant="h4" fontWeight="bold" sx={{ mb: 1 }}>
                {formatCompactCurrency(total_market_cap)}
              </Typography>
              <Chip 
                label="Live Data" 
                size="small" 
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
            color: 'white',
            height: '100%',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: '0 8px 25px rgba(33, 150, 243, 0.3)'
            }
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <ShowChart sx={{ mr: 1, fontSize: 28 }} />
                <Typography variant="h6">24h Volume</Typography>
              </Box>
              <Typography variant="h4" fontWeight="bold" sx={{ mb: 1 }}>
                {formatCompactCurrency(total_volume_24h)}
              </Typography>
              <Chip 
                label="Real-time" 
                size="small" 
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ 
            background: 'linear-gradient(135deg, #FF9800 0%, #F57C00 100%)',
            color: 'white',
            height: '100%',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: '0 8px 25px rgba(255, 152, 0, 0.3)'
            }
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Analytics sx={{ mr: 1, fontSize: 28 }} />
                <Typography variant="h6">Cryptocurrencies</Typography>
              </Box>
              <Typography variant="h4" fontWeight="bold" sx={{ mb: 1 }}>
                {crypto_count}
              </Typography>
              <Chip 
                label="Tracked" 
                size="small" 
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default MarketOverview;