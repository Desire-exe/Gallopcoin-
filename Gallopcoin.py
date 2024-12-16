// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GallopCoinGame is Ownable {
    IERC20 public gallopCoin;
    address public owner;

    mapping(address => uint256) public playerBalances;
    mapping(address => uint256) public stakingBalances;
    mapping(address => uint256) public nftBalances;

    // Events
    event RewardEarned(address indexed player, uint256 amount);
    event NFTMinted(address indexed player, uint256 tokenId);
    event Staked(address indexed player, uint256 amount);
    event Unstaked(address indexed player, uint256 amount);

    constructor(address _gallopCoin) {
        gallopCoin = IERC20(_gallopCoin);
        owner = msg.sender;
    }

    // Reward function to distribute tokens
    function rewardPlayer(address player, uint256 amount) public onlyOwner {
        playerBalances[player] += amount;
        gallopCoin.transfer(player, amount);
        emit RewardEarned(player, amount);
    }

    // Staking function
    function stakeTokens(uint256 amount) public {
        require(gallopCoin.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        stakingBalances[msg.sender] += amount;
        emit Staked(msg.sender, amount);
    }

    // Withdraw staking rewards
    function withdrawStake(uint256 amount) public {
        require(stakingBalances[msg.sender] >= amount, "Insufficient stake");
        stakingBalances[msg.sender] -= amount;
        gallopCoin.transfer(msg.sender, amount);
        emit Unstaked(msg.sender, amount);
    }

    // NFT Minting Functionality (Only owner can mint)
    function mintNFT(address player, uint256 tokenId) public onlyOwner {
        nftBalances[player] += 1;
        emit NFTMinted(player, tokenId);
    }

    // Function to check player balance
    function checkBalance() public view returns (uint256) {
        return playerBalances[msg.sender];
    }

    // Function to check staking balance
    function checkStakingBalance() public view returns (uint256) {
        return stakingBalances[msg.sender];
    }

    // Function to check NFT balance
    function checkNFTBalance() public view returns (uint256) {
        return nftBalances[msg.sender];
    }

    // Admin can pause or resume the contract (for emergencies)
    function pauseContract() public onlyOwner {
        // Add pause logic here (using OpenZeppelin's Pausable contract)
    }

    // Fallback function to accept ETH
    receive() external payable {}
}
